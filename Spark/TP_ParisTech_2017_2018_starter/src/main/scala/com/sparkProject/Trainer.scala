package com.sparkProject


import org.apache.spark.SparkConf
import org.apache.spark.ml.feature._
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator



object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()

    import spark.implicits._
    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    println("hello world ! from Trainer")

    val df: DataFrame = spark
      .read
      .parquet("prepared_trainingset/part-*")

    df.show()

    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")


    // Test:
    val token = tokenizer.transform(df)
       token.show(10)

    val stopwordsremover = new StopWordsRemover()
      .setInputCol("tokens")
      .setOutputCol("filtered")


    // Test :
    val stopword = stopwordsremover.transform(token)
    stopword.show(10)

    val  tf = new CountVectorizer()
      .setInputCol("filtered")
      .setOutputCol("count")

    // Test :

    val tfDf = tf.fit(stopword).transform(stopword)


    val idf = new IDF()
      .setInputCol("count")
      .setOutputCol("tfidf")

    // Test

    val idfDf = idf.fit(tfDf).transform(tfDf)


    val countryIndexer = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")

    val currencyIndexer = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")

    val encoders_country = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("country_onehot")

    val encoders_currency = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currency_onehot")

// Test


    val transformedDf = countryIndexer.fit(idfDf).transform(idfDf)
    val transformedDf2 = currencyIndexer.fit(transformedDf).transform(transformedDf)
    val countryEncodedDf = encoders_country.transform(transformedDf2)
    val encodedDf = encoders_currency.transform(countryEncodedDf)

  //encodedDf.select("country2", "country_indexed", "country_onehot").show(10)
  //encodedDf.select("currency2", "currency_indexed", "currency_onehot").show(10)

    val vector_assembler = new VectorAssembler()
      .setInputCols(Array("tfidf","days_campaign", "hours_prepa", "goal", "country_onehot", "currency_onehot"))
      .setOutputCol("features")

    val vector_assembled = vector_assembler.transform(encodedDf)
    vector_assembled.select("tfidf", "hours_prepa", "features").show(5)



    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    val lrModel = lr.fit(vector_assembled).transform(vector_assembled)
    lrModel.show(5)


    val stages = Array(tokenizer, stopwordsremover, tf, idf, countryIndexer, currencyIndexer, encoders_country, encoders_currency, vector_assembler, lr)
    val pipeline = new Pipeline()
     .setStages(stages)


  val Array(training, test) = df.randomSplit(Array(0.9, 0.1), seed = 1234)

    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(math.pow(10, -8), math.pow(10, -6), math.pow(10, -4), math.pow(10, -2)))
      .addGrid(tf.minDF, Array(55.0, 75.0, 95.0))
      .build()

 val f1Score = new MulticlassClassificationEvaluator()
   .setMetricName("f1")
   .setLabelCol("final_status")
   .setPredictionCol("predictions")

    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(f1Score)
      .setEstimatorParamMaps(paramGrid)
      // 70% of the data will be used for training and the remaining 30% for validation.
      .setTrainRatio(0.7)
      // Evaluate up to 2 parameter settings in parallel
      //.setParallelism(2)

    // Run train validation split, and choose the best set of parameters.

    val model = trainValidationSplit.fit(training)

    // Make predictions on test data. model is the model with combination of parameters
    // that performed best.

    val df_WithPredictions = model.transform(test)
    val f1Score_test = f1Score.evaluate(df_WithPredictions)


    println(s"le f1 score du modèle sur les données de test ${f1Score_test}")

    df_WithPredictions.groupBy("final_status", "predictions").count.show()

  }
}
