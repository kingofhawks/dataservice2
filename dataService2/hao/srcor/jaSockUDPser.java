package srcor;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.*;
import java.io.*;
import java.util.Map;
import java.util.Iterator;
import java.util.Collection;
import java.util.HashMap;
import java.util.Set;
import java.util.Map.Entry;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.awt.Font;
import java.io.FileOutputStream;
/*
import org.jfree.ui.TextAnchor;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.CategoryLabelPositions;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.title.TextTitle;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.chart.renderer.category.BarRenderer3D;
import org.jfree.chart.labels.StandardCategoryItemLabelGenerator;
import org.jfree.chart.labels.ItemLabelPosition;
import org.jfree.chart.labels.ItemLabelAnchor;
*/
public class jaSockUDPser {
	public static String recv() throws Exception {
		DatagramSocket ds = new DatagramSocket(12220);
		byte[] buf = new byte[1024];
		DatagramPacket dp = new DatagramPacket(buf, 1024);
		ds.receive(dp);
		String msg = new String(buf, 0, 1024);
		System.out.println(msg);
		ds.close();
		send("clean history");
		return msg;
	}

	public static void send(String msg) throws Exception {
		DatagramSocket ds = new DatagramSocket();
		DatagramPacket dp = new DatagramPacket(msg.getBytes(), msg.length(),
				InetAddress.getByName("192.168.0.95"), 12224);
		ds.send(dp);
		ds.close();
	}

	public static String ec(String command) throws InterruptedException {
		String returnString = "";
		Process pro = null;
		Runtime runTime = Runtime.getRuntime();
		if (runTime == null) {
			System.err.println("Create runtime false!");
		}
		try {
			runTime.traceInstructions(true);
			System.out.println(command);
			pro = runTime.exec(command);
			BufferedReader input = new BufferedReader(new InputStreamReader(
					pro.getInputStream()));
			PrintWriter output = new PrintWriter(new OutputStreamWriter(
					pro.getOutputStream()));
			String line;
			while ((line = input.readLine()) != null) {
				returnString = returnString + line + "\n";
			}
			input.close();
			output.close();
			pro.destroy();
		} catch (IOException ex) {
			Logger.getLogger(jaSockUDPser.class.getName()).log(Level.SEVERE,
					null, ex);
			returnString = "run command error";
		}
		return returnString;
	}

	public static boolean parseMsg(String msg, Map<String, Set<String>> m_para)
			throws Exception {
		StringTokenizer tokenizer = new StringTokenizer(msg, "#");
		System.out.println(tokenizer.countTokens());
		if (tokenizer.countTokens() != 6) {// if miss input data, alg file or
											// output directory
			try {
				send("miss parameters!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		String token = tokenizer.nextToken();
		String addr = tokenizer.nextToken();
		String algFiles = tokenizer.nextToken();
		String dataFiles = tokenizer.nextToken();
		String outputDir = tokenizer.nextToken();

		StringTokenizer tokenizer_token = new StringTokenizer(token, "$");
		String str_sign_token = tokenizer_token.nextToken();
		String str_token = tokenizer_token.nextToken();

		StringTokenizer tokenizer_addr = new StringTokenizer(addr, "$");
		String str_sign_addr = tokenizer_addr.nextToken();
		String str_addr = tokenizer_addr.nextToken();
		// ----------------------token and address-------------------------
		if (str_token == null || str_token.equals("") || str_addr == null
				|| str_addr.equals("")) {
			try {
				send("miss token or container address!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		Set<String> set_token = new HashSet<String>();
		set_token.add(str_token);
		m_para.put(str_sign_token, set_token);
		Set<String> set_addr = new HashSet<String>();
		set_addr.add(str_addr);
		m_para.put(str_sign_addr, set_addr);
		// ------------algrithms files------------------------
		StringTokenizer tokenizer_alg = new StringTokenizer(algFiles, "$");
		if (tokenizer_alg.countTokens() != 2) {
			try {
				send("miss alg parameters! alg:alg1,alg2,....!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		String str_sign_alg = tokenizer_alg.nextToken();
		String str_algs = tokenizer_alg.nextToken();

		StringTokenizer tokenizer_alg_file = new StringTokenizer(str_algs, ",");
		if (tokenizer_alg_file.countTokens() < 1) {
			try {
				send("miss alg parameters! alg:alg1,alg2,....!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}

		}
		Set<String> set_alg_files = new HashSet<String>();
		int num_class_file = 0;
		int num_java_file = 0;
		int num_jar_file = 0;
		int num_items_file = 0;
		while (tokenizer_alg_file.hasMoreTokens()) {
			String str_alg_file = tokenizer_alg_file.nextToken();
			set_alg_files.add(str_alg_file);
			if (str_alg_file.contains(".class")) {
				num_class_file++;
			}
			if (str_alg_file.contains(".java")) {
				num_java_file++;
			}
			if (str_alg_file.contains(".jar")) {
				num_jar_file++;
			}
			if (str_alg_file.contains(".items")) {
				num_items_file++;
			}
		}
		m_para.put(str_sign_alg, set_alg_files);
		if (num_java_file > 1) {
			send("error: more than one .java file...");
			send("#fail#");
			return false;
		}
		if (num_jar_file != 1) {
			send("error: no or more than one .jar file...");
			send("#fail#");
			return false;
		}
		if (num_items_file != 1) {
			send("error: no or more than one .items file...");
			send("#fail#");
			return false;
		}
		if (num_class_file > 1) {
			send("error: more than one .class file...");
			send("#fail#");
			return false;
		}
		if (num_java_file == 0 && num_class_file == 0) {
			send("error: no .java file or .class file is specified...");
			send("#fail#");
			return false;
		}
		// ----------------data files---------------------
		StringTokenizer tokenizer_data = new StringTokenizer(dataFiles, "$");
		if (tokenizer_data.countTokens() < 1) {
			try {
				send("miss data parameters! data:data1,data2,....!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}

		}
		String str_sign_data = tokenizer_data.nextToken();
		String str_data = tokenizer_data.nextToken();

		StringTokenizer tokenizer_data_file = new StringTokenizer(str_data, ",");
		if (tokenizer_data_file.countTokens() < 1) {
			try {
				send("miss data parameters! data:data1,data2,....!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}

		}
		Set<String> set_data_files = new HashSet<String>();
		while (tokenizer_data_file.hasMoreTokens()) {
			set_data_files.add(tokenizer_data_file.nextToken());
		}
		m_para.put(str_sign_data, set_data_files);
		// -----------------output directory--------------------
		StringTokenizer tokenizer_output = new StringTokenizer(outputDir, "$");
		if (tokenizer_output.countTokens() != 2) {
			try {
				send("specify  one and only one output directory!");
				send("#fail#");
				return false;
			} catch (Exception e) {
				e.printStackTrace();
			}

		}
		String str_sign_output = tokenizer_output.nextToken();
		String str_output = tokenizer_output.nextToken();
		Set<String> set_output_dir = new HashSet<String>();
		set_output_dir.add(str_output);
		m_para.put(str_sign_output, set_output_dir);
		return true;
	}

	public static boolean prepareFiles(Map<String, Set<String>> m_para)
			throws Exception {
		send("preparing data files and algorithms files!");
		String intermedia_get_data = "get_data.sh";
		String inputdataDir = "inputdata";
		String algFileDir = "alg";
		String mkdir_inputdataDir = "mkdir " + inputdataDir;
		String mkdir_algFileDir = "mkdir " + algFileDir;

		String exec_mkdir_inputdata = ec(mkdir_inputdataDir);// mkdir inputdata
		String exec_mkdir_algDir = ec(mkdir_algFileDir);// mkdir alg

		Set<String> set_token = m_para.get("token");
		Iterator iter_set_token = set_token.iterator();
		String str_token = iter_set_token.next().toString();
		Set<String> set_addr = m_para.get("URL");
		Iterator iter_set_addr = set_addr.iterator();
		String str_addr = iter_set_addr.next().toString();

		Set<String> set_data = m_para.get("data");
		Iterator iter_set_data = set_data.iterator();

		Set<String> set_alg = m_para.get("alg");
		Iterator iter_set_alg = set_alg.iterator();

		BufferedWriter bufwt_intermedia_get_data = new BufferedWriter(
				new FileWriter(intermedia_get_data));
		bufwt_intermedia_get_data.write("#!/usr/bin/env bash");
		bufwt_intermedia_get_data.newLine();
		while (iter_set_data.hasNext()) {
			String str_data_name = iter_set_data.next().toString();
			String storage_get = "curl -X GET -H 'X-Auth-Token:" + str_token
					+ "' " + str_addr + "/datafiles/" + str_data_name + " > "
					+ inputdataDir + "/" + str_data_name;
			try {
				bufwt_intermedia_get_data.write(storage_get);
				bufwt_intermedia_get_data.newLine();
			} catch (Exception e) {
				e.printStackTrace();
				send("error: write intermedia files error, please check  priority of user...");
				send("#fail#");
				return false;
			}
		}
		while (iter_set_alg.hasNext()) {
			String str_alg_name = iter_set_alg.next().toString();
			String storage_get = "curl -X GET -H 'X-Auth-Token:" + str_token
					+ "' " + str_addr + "/algo/" + str_alg_name + " > "
					+ algFileDir + "/" + str_alg_name;
			try {
				bufwt_intermedia_get_data.write(storage_get);
				bufwt_intermedia_get_data.newLine();
			} catch (Exception e) {
				e.printStackTrace();
				send("error: write intermedia files error, please check  priority of user...");
				send("#fail#");
				return false;
			}

		}
		bufwt_intermedia_get_data.close();
		String make_runable = "chmod a+x " + intermedia_get_data;
		String aa = ec(make_runable);// change mod to executable
		aa = ec("./" + intermedia_get_data);// run the shell script
		Iterator iter_set_data_check = set_data.iterator();
		while (iter_set_data_check.hasNext()) {
			String str_data_name = iter_set_data_check.next().toString();
			File data_file = new File(inputdataDir + "/" + str_data_name);
			if (!data_file.exists()) {
				send("error: can't get data files from storage platform!");
				send("#fail#");
				return false;
			}
		}
		Iterator iter_set_alg_check = set_alg.iterator();
		while (iter_set_alg_check.hasNext()) {
			String str_alg_name = iter_set_alg_check.next().toString();
			File alg_file = new File(algFileDir + "/" + str_alg_name);
			if (!alg_file.exists()) {
				send("error: can't get algorithms files from storage platform!");
				send("#fail#");
				return false;
			}
			if (str_alg_name.contains(".items")) {// copy .items file to hdfs
				String change_name = "cp " + algFileDir + "/" + str_alg_name
						+ " items.txt";
				String hdfs_make_items_dir = "hadoop dfs -mkdir items";
				String hdfs_put_items = "hadoop dfs -put items.txt items";
				try {
					aa = ec(change_name);
					aa = ec(hdfs_make_items_dir);
					aa = ec(hdfs_put_items);
				} catch (Exception e) {
					send("error: run Hadoop MapReduce Command error, please check the priority of user...");
					send("#fail#");
					return false;
				}
			}
		}
		aa = ec("rm " + intermedia_get_data);// remove shell script
		// ------------------add to map-----------------
		Set<String> set_input_dir = new HashSet<String>();
		set_input_dir.add(inputdataDir);
		m_para.put("input_dir", set_input_dir);
		Set<String> set_alg_dir = new HashSet<String>();
		set_alg_dir.add(algFileDir);
		m_para.put("alg_dir", set_alg_dir);
		// ---------------------put data to hdfs--------------------
		String hdfs_mkdir_inputdata = "hadoop dfs -mkdir " + inputdataDir;
		aa = ec(hdfs_mkdir_inputdata);
		Iterator iter_set_data_put = set_data.iterator();
		while (iter_set_data_put.hasNext()) {
			String str_data_name = iter_set_data_put.next().toString();
			String hdfs_put_data = "hadoop dfs -put " + inputdataDir + "/"
					+ str_data_name + " " + inputdataDir;
			try {
				aa = ec(hdfs_put_data);
			} catch (Exception e) {
				send("error: run Hadoop MapReduce Command error, please check the priority of user...");
				send("#fail#");
				return false;
			}
		}
		// --------------rm local input data---------------
		String rm_local_inputdata = "rm -r " + inputdataDir;
		try {
			aa = ec(rm_local_inputdata);
		} catch (Exception e) {
			send("error: run Hadoop MapReduce Command error, please check the priority of user...");
			send("#fail#");
			return false;
		}

		send("data files and algorithms files are ready!");
		return true;
	}

	public static boolean runAlg(Map<String, Set<String>> m_para)
			throws Exception {
		send("starting to run algorithm");
		// -------------------alg files check -----------------
		Set<String> m_s_alg_value = m_para.get("alg");
		Iterator iter_s_alg_value = m_s_alg_value.iterator();
		int num_class_file = 0;
		String class_file_name = null;
		int num_java_file = 0;
		String java_file_name = null;
		int num_jar_file = 0;
		String jar_file_name = null;
		int num_items_file = 0;
		String items_file_name = null;
		String alg_dir = null;

		Set<String> m_s_alg_dir = m_para.get("alg_dir");
		Iterator iter_s_alg_dir = m_s_alg_dir.iterator();
		alg_dir = iter_s_alg_dir.next().toString();

		while (iter_s_alg_value.hasNext()) {
			String str_alg_value = iter_s_alg_value.next().toString();
			if (str_alg_value.contains(".class")) {
				num_class_file++;
				class_file_name = str_alg_value;
				continue;
			}
			if (str_alg_value.contains(".java")) {
				num_java_file++;
				java_file_name = str_alg_value;
				continue;
			}
			if (str_alg_value.contains(".jar")) {
				num_jar_file++;
				jar_file_name = str_alg_value;
				continue;
			}
			if (str_alg_value.contains(".items")) {
				num_items_file++;
				items_file_name = str_alg_value;
				continue;
			}
		}
		if (num_java_file > 1 || num_class_file > 1 || num_items_file > 1) {
			send("alg files error! more than one executable alg file or items file");
			send("#fail#");
			rmTrash();
			return false;
		}
		if (num_jar_file != 1) {
			send("alg files error! no .jar file");
			send("#fail#");
			rmTrash();
			return false;
		}
		if (num_items_file != 1) {
			send("alg files error! no .items file");
			send("#fail#");
			rmTrash();
			return false;
		}
		if (num_java_file == 0 && num_class_file == 0) {
			send("alg files error! no .java or .class file");
			send("#fail#");
			rmTrash();
			return false;
		}
		if (num_java_file == 1 && num_class_file == 0) {
			int index = java_file_name.indexOf(".");
			String alg_name = java_file_name.substring(0, index);
			String run_javac = "javac " + alg_dir + "/" + java_file_name;
			String run_javac_output = "result: ";
			try {
				run_javac_output = run_javac_output + ec(run_javac);
			} catch (Exception e) {
				send("error: compile .java file error...");
				send("#fail#");
				return false;
			}

			index = jar_file_name.indexOf(".");
			String jar_name = jar_file_name.substring(0, index);

			Set<String> m_s_data_value = m_para.get("input_dir");
			Iterator iter_s_data_value = m_s_data_value.iterator();
			String inputdata_dir = iter_s_data_value.next().toString();

			Set<String> m_s_out_value = m_para.get("outfile");
			Iterator iter_s_out_value = m_s_out_value.iterator();
			String outputdata_dir = iter_s_out_value.next().toString();

			String run_alg = "java " + "-cp " + alg_dir + " " + alg_name + " "
					+ jar_file_name + " " + jar_name + " " + inputdata_dir
					+ " " + outputdata_dir + " -item items/items.txt 0.01";
			try {
				String run_hadoop_msg = ec(run_alg);
				System.out.println(run_hadoop_msg);
			} catch (Exception e) {
				send("error: run Hadoop MapReduce error...");
				send("#fail#");
				return false;
			}
		}
		if (num_class_file == 1) {
			int index = class_file_name.indexOf(".");
			String alg_name = class_file_name.substring(0, index);

			index = jar_file_name.indexOf(".");
			String jar_name = jar_file_name.substring(0, index);

			Set<String> m_s_data_value = m_para.get("input_dir");
			Iterator iter_s_data_value = m_s_data_value.iterator();
			String inputdata_dir = iter_s_data_value.next().toString();

			Set<String> m_s_out_value = m_para.get("outfile");
			Iterator iter_s_out_value = m_s_out_value.iterator();
			String outputdata_dir = iter_s_out_value.next().toString();

			String run_alg = "java " + "-cp " + alg_dir + " " + alg_name + " "
					+ jar_file_name + " " + jar_name + " " + inputdata_dir
					+ " " + outputdata_dir + " -item items/items.txt 0.01";
			try {
				String run_hadoop_msg = ec(run_alg);
				System.out.println(run_hadoop_msg);
			} catch (Exception e) {
				send("error: run Hadoop MapReduce error...");
				send("#fail#");
				return false;
			}

			// send("finish running algorithms");

		}
		send("finish running algorithms");
		return true;
	}

	public static boolean checkOutput(Map<String, Set<String>> m_para)
			throws Exception {
		File output_confi = new File("confidenceres.txt");
		File output_supp = new File("res.txt");
		if (!output_confi.exists() || !output_supp.exists()) {
			send("analyze failed, please double check your algorithms files and make the .items file match the inputdata...");
			send("#fail#");
			rmTrash();
			return false;
		}
		Set<String> m_s_out_value = m_para.get("out");
		Iterator iter_s_out_value = m_s_out_value.iterator();
		String outputdata_dir = iter_s_out_value.next().toString();
		String mkdir_outputdata_dir = "";
		String upload_outputdata = "";
		return true;
	}
/*
	public static boolean paintSupport() throws Exception {
		DefaultCategoryDataset dataset = new DefaultCategoryDataset();
		BufferedReader buf_rd = null;
		double paint_factor = 0.01;
		String line = null;
		try {
			buf_rd = new BufferedReader(new FileReader("res.txt"));
		} catch (Exception e) {
			System.out.println("can't read file for painting!");
			send("paint failed");
			return false;
		}
		while ((line = buf_rd.readLine()) != null) {
			int i = 0;
			String str_value = null;
			StringTokenizer str_token_line = new StringTokenizer(line);
			while (str_token_line.hasMoreTokens()) {
				str_value = str_token_line.nextToken();
			}
			String str_item = line.replace(str_value, "");
			double doub_value = Double.parseDouble(str_value);
			if (doub_value >= paint_factor) {
				dataset.addValue(doub_value, "", str_item);
			}
		}
		JFreeChart chart = ChartFactory.createBarChart3D("support", "items",
				"value(0-1)", dataset, PlotOrientation.VERTICAL, false, false,
				false);
		chart.setTitle(new TextTitle("support", new Font("Times New Roman",
				Font.BOLD, 22)));
		CategoryPlot plot = (CategoryPlot) chart.getPlot();

		BarRenderer3D customBarRenderer = (BarRenderer3D) plot.getRenderer();
		customBarRenderer
				.setBaseItemLabelGenerator(new StandardCategoryItemLabelGenerator());
		customBarRenderer.setBaseItemLabelsVisible(true);
		customBarRenderer
				.setBasePositiveItemLabelPosition(new ItemLabelPosition(
						ItemLabelAnchor.OUTSIDE12, TextAnchor.BASELINE_CENTER));
		customBarRenderer.setItemLabelAnchorOffset(10D);
		customBarRenderer.setItemLabelsVisible(true);
		CategoryAxis categoryAxis = plot.getDomainAxis();
		categoryAxis.setLabelFont(new Font("Times New Roman", Font.BOLD, 15));

		categoryAxis.setCategoryLabelPositions(CategoryLabelPositions.UP_45);
		categoryAxis
				.setTickLabelFont(new Font("Times New Roman", Font.BOLD, 12));

		NumberAxis numberAxis = (NumberAxis) plot.getRangeAxis();
		numberAxis.setLabelFont(new Font("Times New Roman", Font.BOLD, 20));

		FileOutputStream fos = null;
		fos = new FileOutputStream("support.jpg");
		File web_support = new File(
				"/usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/dmimg/support.jpg");
		if (web_support.exists()) {
			try {
				web_support.delete();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		// fos_web = new
		// FileOutputStream("/usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/dmimg/support.jpg");
		ChartUtilities.writeChartAsJPEG(fos, 1, chart, 1260, 1024, null);
		fos.close();

		FileOutputStream fos_web = null;
		fos_web = new FileOutputStream(
				"/usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/dmimg/support.jpg");
		ChartUtilities.writeChartAsJPEG(fos_web, 1, chart, 1260, 1024, null);
		fos_web.close();
		send("generate support.jpg");
		return true;
	}*/

	public static boolean uploadOutput(Map<String, Set<String>> m_para)
			throws Exception {
		String str_confi = "confidenceres.txt";
		String str_res = "res.txt";
		String str_paint = "support.jpg";
		String outputdata_dir = null;
		String upload_confi = null;
		String upload_res = null;
		String upload_paint = null;
		String mkdir_outputdata = null;
		String intermedia_put_data = "put_data.sh";
		String msg = "";

		Set<String> set_token = m_para.get("token");
		Iterator iter_set_token = set_token.iterator();
		String str_token = iter_set_token.next().toString();
		Set<String> set_addr = m_para.get("URL");
		Iterator iter_set_addr = set_addr.iterator();
		String str_addr = iter_set_addr.next().toString();
		Set<String> m_s_out_value = m_para.get("outfile");
		Iterator iter_s_out_value = m_s_out_value.iterator();
		outputdata_dir = iter_s_out_value.next().toString();

		mkdir_outputdata = "curl -X PUT -H 'X-Auth-Token:" + str_token + "' "
				+ str_addr + "/" + outputdata_dir;
		upload_confi = "curl -X PUT -H 'X-Auth-Token:" + str_token + "' -T "
				+ "'" + str_confi + "' " + str_addr + "/" + outputdata_dir
				+ "/" + "confidence.txt";
		upload_res = "curl -X PUT -H 'X-Auth-Token:" + str_token + "' -T "
				+ "'" + str_res + "' " + str_addr + "/" + outputdata_dir + "/"
				+ "support.txt";
		upload_paint = "curl -X PUT -H 'X-Auth-Token:" + str_token + "' -T "
				+ "'" + str_paint + "' " + str_addr + "/" + outputdata_dir
				+ "/" + "support.jpg";
		try {
			BufferedWriter bufwt_intermedia_put_data = new BufferedWriter(
					new FileWriter(intermedia_put_data));
			bufwt_intermedia_put_data.write("#!/usr/bin/env bash");
			bufwt_intermedia_put_data.newLine();
			bufwt_intermedia_put_data.write(mkdir_outputdata);
			bufwt_intermedia_put_data.newLine();
			bufwt_intermedia_put_data.write(upload_confi);
			bufwt_intermedia_put_data.newLine();
			bufwt_intermedia_put_data.write(upload_res);
			bufwt_intermedia_put_data.newLine();
			bufwt_intermedia_put_data.write(upload_paint);
			bufwt_intermedia_put_data.close();

			msg = ec("chmod a+x " + intermedia_put_data);
			msg = ec("./" + intermedia_put_data);
			msg = ec("rm " + intermedia_put_data);
			send("finish all the work! output files are stored in "
					+ outputdata_dir);
			send("#success#");
		} catch (Exception e) {
			e.printStackTrace();
			send("error: can't save results to storage platform...");
			send("#fail#");
			return false;
		}
		return true;
	}

	public static void rmTrash() throws Exception {
		String msg = null;
		File rm_file = null;
		rm_file = new File("confidenceres.txt");
		if (rm_file.exists()) {
			rm_file.delete();
		}
		rm_file = new File("res.txt");
		if (rm_file.exists()) {
			rm_file.delete();
		}
		rm_file = new File("support.jpg");
		if (rm_file.exists()) {
			rm_file.delete();
		}
		rm_file = new File("alg");
		if (rm_file.isDirectory()) {
			File files[] = rm_file.listFiles();
			for (int i = 0; i < files.length; i++) {
				files[i].delete();
			}
			rm_file.delete();
		}
		msg = ec("hadoop dfs -rmr inputdata");
	}

	public static void main(String[] args) throws Exception {
		while (true) {
			Map<String, Set<String>> m_para = new HashMap<String, Set<String>>();
			String msg = recv();
			if (!parseMsg(msg, m_para)) {
				continue;
			}
			if (!prepareFiles(m_para)) {
				continue;
			}
			if (!runAlg(m_para)) {
				continue;
			}
			/*
			if (!paintSupport()) {
				continue;
			}
			*/
			if (!uploadOutput(m_para)) {
				continue;
			}
			rmTrash();
		}
	}
}
