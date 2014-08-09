package srcor;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.util.StringUtils;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class jacts extends Configured implements Tool {
	public int run(String[] paramArrayOfString) throws Exception {
		JobConf localJobConf = new JobConf(getConf(), jacts.class);
		localJobConf.setJobName("jacts");

		localJobConf.setOutputKeyClass(Text.class);
		localJobConf.setOutputValueClass(IntWritable.class);

		localJobConf.setMapperClass(jacts.Map.class);
		localJobConf.setCombinerClass(jacts.Reduce.class);
		localJobConf.setReducerClass(jacts.Reduce.class);

		localJobConf.setInputFormat(TextInputFormat.class);
		localJobConf.setOutputFormat(TextOutputFormat.class);

		ArrayList localArrayList = new ArrayList();
		for (int i = 0; i < paramArrayOfString.length; i++) {
			if ("-item".equals(paramArrayOfString[i])) {
				DistributedCache.addCacheFile(new Path(
						paramArrayOfString[(++i)]).toUri(), localJobConf);
				localJobConf.setBoolean("jacts.use.items", true);
			} else {
				localArrayList.add(paramArrayOfString[i]);
			}
		}
		FileInputFormat.setInputPaths(localJobConf, new Path[] { new Path(
				(String) localArrayList.get(0)) });
		FileOutputFormat.setOutputPath(localJobConf, new Path(
				(String) localArrayList.get(1)));

		JobClient.runJob(localJobConf);
		return 0;
	}

	public static void main(String[] paramArrayOfString) throws Exception {
		int i = ToolRunner.run(new Configuration(), new jacts(),
				paramArrayOfString);
		System.exit(i);
	}

	public static class Reduce extends MapReduceBase implements
			Reducer<Text, IntWritable, Text, IntWritable> {
		public void reduce(Text paramText, Iterator<IntWritable> paramIterator,
				OutputCollector<Text, IntWritable> paramOutputCollector,
				Reporter paramReporter) throws IOException {
			int i = 0;
			while (paramIterator.hasNext()) {
				i += ((IntWritable) paramIterator.next()).get();
			}
			paramOutputCollector.collect(paramText, new IntWritable(i));
		}
	}

	public static class Map extends MapReduceBase implements
			Mapper<LongWritable, Text, Text, IntWritable> {
		private static final IntWritable one = new IntWritable(1);
		private Text t_sum = new Text("overall");
		private Text item = new Text();

		private Set<String> itemsToAnalyze = new HashSet();
		private String inputFile;
		private long numRecords = 0L;

		public void configure(JobConf paramJobConf) {
			this.inputFile = paramJobConf.get("map.input.file");
			if (paramJobConf.getBoolean("jacts.use.items", false)) {
				Path[] arrayOfPath1 = new Path[0];
				try {
					arrayOfPath1 = DistributedCache
							.getLocalCacheFiles(paramJobConf);
				} catch (IOException localIOException) {
					System.err
							.println("Caught exception while getting cached files: "
									+ StringUtils
											.stringifyException(localIOException));
				}
				for (Path localPath : arrayOfPath1)
					parseAnalyzeFile(localPath);
			}
		}

		private void parseAnalyzeFile(Path paramPath) {
			try {
				BufferedReader localBufferedReader = new BufferedReader(
						new FileReader(paramPath.toString()));
				String str1 = null;
				while ((str1 = localBufferedReader.readLine()) != null) {
					int i = str1.indexOf(":");
					int j = str1.length();
					if ((i < 1) || (i > j)) {
						System.out.println("items file error: no group number");
						System.exit(1);
					}
					String str2 = str1.substring(i + 1, j);
					this.itemsToAnalyze.add(str2);
				}
			} catch (IOException localIOException) {
				System.err
						.println("Caught exception while parsing the cached file '"
								+ paramPath
								+ "' : "
								+ StringUtils
										.stringifyException(localIOException));
			}
		}

		public void map(LongWritable paramLongWritable, Text paramText,
				OutputCollector<Text, IntWritable> paramOutputCollector,
				Reporter paramReporter) throws IOException {
			String str1 = paramText.toString();
			if (str1 != null)
				paramOutputCollector.collect(this.t_sum, one);
			for (String str2 : this.itemsToAnalyze) {
				Object localObject1;
				if (str2.contains("&&")) {
					localObject1 = new StringTokenizer(str2, "&&");
					int i = ((StringTokenizer) localObject1).countTokens();
					int j = 0;
					Object localObject2;
					while (((StringTokenizer) localObject1).hasMoreTokens()) {
						localObject2 = ((StringTokenizer) localObject1)
								.nextToken();
						if (str1.contains((CharSequence) localObject2)) {
							j++;
						} else if (((String) localObject2).contains("||")) {
							StringTokenizer localStringTokenizer = new StringTokenizer(
									(String) localObject2, "||");
							while (localStringTokenizer.hasMoreTokens()) {
								if (str1.contains(localStringTokenizer
										.nextToken())) {
									j++;
								}
							}
						}
					}

					if (i == j) {
						localObject2 = new Text(str2);
						paramOutputCollector.collect(localObject2, one);
					}
				} else if (str1.contains(str2)) {
					localObject1 = new Text(str2);
					paramOutputCollector.collect(localObject1, one);
				} else if (str2.contains("||")) {
					localObject1 = new StringTokenizer(str2, "||");
					while (((StringTokenizer) localObject1).hasMoreTokens())
						if (str1.contains(((StringTokenizer) localObject1)
								.nextToken())) {
							Text localText = new Text(str2);
							paramOutputCollector.collect(localText, one);
						}
				}
			}
		}
	}
}