import org.apache.iceberg.hive.HiveCatalog;




val catalog = new HiveCatalog(spark.sparkContext().hadoopConfiguration());


import org.apache.iceberg.Table;
import org.apache.iceberg.catalog.TableIdentifier;

val name = TableIdentifier.of("logging", "logs");
val table = catalog.createTable(name, schema, spec);

// or to load an existing table, use the following line
// Table table = catalog.loadTable(name);