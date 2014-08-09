package srcor;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.*;
import java.io.*;
import java.util.Map;
import java.util.Iterator;
import java.util.Collection;
import java.util.HashMap;
import java.util.Set;
import java.util.Map.Entry;
import java.text.DecimalFormat;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class algcts {
	public static Map<String, Set> m_sign_item = new HashMap<String, Set>();
	public static Map<String, Map> m_m_output = new HashMap<String, Map>();
	public static Map<String, Map> m_m_support = new HashMap<String, Map>();
	public static int count_prune = 0;

	public static String ec(String command) throws InterruptedException {
		String returnString = "";
		Process pro = null;
		Runtime runTime = Runtime.getRuntime();
		if (runTime == null) {
			System.err.println("Create runtime false!");
		}
		try {
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
			Logger.getLogger(algcts.class.getName())
					.log(Level.SEVERE, null, ex);
			System.out.println("error: run command");
		}
		return returnString;
	}

	public static void send(String msg) throws Exception {
		DatagramSocket ds = new DatagramSocket();
		DatagramPacket dp = new DatagramPacket(msg.getBytes(), msg.length(),
				InetAddress.getByName("192.168.0.95"), 12224);
		ds.send(dp);
		ds.close();
	}

	public static boolean copyOutput(String output_path, String tmp_item_path)
			throws Exception {
		String dfs_path = output_path + "/part-00000";
		String local_path = "level1";
		String str_cmd = "hadoop dfs -get " + dfs_path + " " + local_path;
		String str_cmd_tmp_item = "hadoop dfs -get " + tmp_item_path + " "
				+ "items.txt";
		String res_msg = null;
		if (!tmp_item_path.equals("none")) {
			File f_rm = new File("items.txt");
			f_rm.delete();
			res_msg = ec(str_cmd_tmp_item);
			File f_rm_out = new File("level1");
			if (f_rm_out.exists()) {
				f_rm_out.delete();
			}
		}
		res_msg = ec(str_cmd);
		File f = new File(local_path);
		boolean file_exist = f.exists();
		if (file_exist == false) {
			System.out.println("error: output file does not exist!");
			return false;
		}
		return true;
	}

	public static boolean judgePrune(double effect_factor, List<String> top_sign)
			throws Exception {
		String local_path = "level1";
		String item_path = "items.txt";
		String intermedia_file = "tmp.txt";
		String str_res = null;
		String line = null;
		List<String> l_continue = new ArrayList<String>();
		List<String> l_delete = new ArrayList<String>();
		Map<String, String> m_res = new HashMap<String, String>();
		BufferedReader bufrd = new BufferedReader(new FileReader(local_path));
		// -----------------read output file--------------------
		while ((str_res = bufrd.readLine()) != null) {
			StringTokenizer tokenizer = new StringTokenizer(str_res);
			int num = tokenizer.countTokens();
			int i = 0;
			String key = "";
			String value = "";
			for (i = 0; i < num - 1; i++) {// concat the first num-1 tokenizers
				if (tokenizer.hasMoreTokens()) {
					key = key + tokenizer.nextToken();
				}// endif
			}// end for
			if (tokenizer.hasMoreTokens()) {
				value = tokenizer.nextToken();
			}
			m_res.put(key, value);
			System.out.println(key + ":" + value);// test
		}// end while
		bufrd.close();
		// -------------read file: items.txt----------------
		BufferedReader bufrd_items = new BufferedReader(new FileReader(
				item_path));
		Set<String> itemsToAnalyze = new HashSet<String>();
		Map<String, Set> m_ss = new HashMap<String, Set>();// contains group
															// sign as key and
															// all the numbers
															// as values
		// remove space between words
		while ((line = bufrd_items.readLine()) != null) {
			StringTokenizer tokenizer = new StringTokenizer(line);
			String str = "";
			while (tokenizer.hasMoreTokens()) {
				str = str + tokenizer.nextToken();
			}
			itemsToAnalyze.add(str);
		}
		bufrd_items.close();
		String sum_value = m_res.get("overall").toString();
		double doub_sum_value = Double.parseDouble(sum_value);// sum
		List<String> l_sign = new ArrayList<String>();
		for (String item : itemsToAnalyze) {
			int group_sign_index = item.indexOf(":");
			int item_len = item.length();
			if (group_sign_index < 1 || group_sign_index > item_len) {
				System.out.println("items file error: no group number");
				System.exit(1);
			}
			String str_cont = item.substring(group_sign_index + 1, item_len);
			String str_sign = item.substring(0, group_sign_index);
			System.out.println("items: " + str_cont);// test
			String v = m_res.get(str_cont);
			if (v == null) {
				v = "0";
			}
			System.out.println("get value by items: " + v);// test
			double doub_v = Double.parseDouble(v);
			double doub_v_per = doub_v / doub_sum_value;
			String str_v = Double.toString(doub_v_per);
			if (!m_ss.containsKey(str_sign)) {
				l_sign.add(str_sign);
				Set<String> s_s = new HashSet<String>();
				s_s.add(v);
				m_ss.put(str_sign, s_s);
				// create a new output map item
				Map<String, String> m_ss_output = new HashMap<String, String>();
				m_ss_output.put(str_cont, str_v);
				m_m_output.put(str_sign, m_ss_output);
			} else {
				Set<String> s_s = m_ss.get(str_sign);
				s_s.add(v);
				// add to a existing output map item
				Map<String, String> m_ss_output = m_m_output.get(str_sign);
				m_ss_output.put(str_cont, str_v);
			}
		}// end for
		Iterator iter_l = l_sign.iterator();
		while (iter_l.hasNext()) {
			String str_sign = iter_l.next().toString();
			Set<String> s_s = m_ss.get(str_sign);
			Iterator iter_s = s_s.iterator();// null exception
			double max = -1;
			double min = 2;
			while (iter_s.hasNext()) {
				double doub_value = Double
						.parseDouble(iter_s.next().toString());
				System.out.print(str_sign + ":	");// test
				System.out.println(doub_value);// test

				if (doub_value / doub_sum_value > max) {
					max = doub_value / doub_sum_value;
				}
				if (doub_value / doub_sum_value < min) {
					min = doub_value / doub_sum_value;
				}
			}
			double sub_max_min = max - min;
			System.out.print(str_sign + ":	");// test
			System.out.println(sub_max_min);// test
			if (sub_max_min > effect_factor) {
				l_continue.add(str_sign);
			} else {
				l_delete.add(str_sign);
				m_m_output.remove(str_sign);// rm this map item from output
			}
		}
		// -------------get sign item (description of item) according to group
		// sign------------------
		BufferedReader bufrd_item_sc = new BufferedReader(new FileReader(
				item_path));
		while ((line = bufrd_item_sc.readLine()) != null) {
			Iterator iter_l_sign = l_sign.iterator();
			while (iter_l_sign.hasNext()) {
				String group_sign = iter_l_sign.next().toString();
				if (line.contains(group_sign)) {
					String trimed_line = line.replace(group_sign + ":", "");
					if (!m_sign_item.containsKey(group_sign)) {
						Set<String> s_item = new HashSet<String>();
						s_item.add(trimed_line);
						m_sign_item.put(group_sign, s_item);
					} else {
						Set<String> s_item = m_sign_item.get(group_sign);
						s_item.add(trimed_line);
					}
				}
			}
		}
		// ----------------------test---------------------
		Iterator iter_l_sign = l_sign.iterator();
		System.out.println("---------sign item map ------------");
		while (iter_l_sign.hasNext()) {
			Set<String> s_item = m_sign_item.get(iter_l_sign.next());
			Iterator iter = s_item.iterator();
			while (iter.hasNext()) {
				System.out.println(iter.next());
			}
		}
		// ---------------test--------------
		System.out.println("-----------l-continue----------");
		int num_continue = l_continue.size();
		System.out.println(num_continue);
		Iterator l_print_continue = l_continue.iterator();
		while (l_print_continue.hasNext()) {
			System.out.println(l_print_continue.next());
		}
		// ------------------------test------------------
		System.out.println("------------write intermedia file------------");//
		if (num_continue <= 1) {
			System.out.println("finish all task");
			System.out.println("writing output");
			return false;
		} else {
			int i, j;
			BufferedWriter bufwt_intermedia = new BufferedWriter(
					new FileWriter(intermedia_file));
			for (i = 0; i < num_continue; i++) {
				int top_sign_index = -1;
				String str_sign_fore = l_continue.get(i).toString();
				Iterator iter_top_sign = top_sign.iterator();
				while (iter_top_sign.hasNext()) {
					String str_top_sign = iter_top_sign.next().toString();
					if (str_sign_fore.contains(str_top_sign)
							&& top_sign.indexOf(str_top_sign) > top_sign_index) {
						top_sign_index = top_sign.indexOf(str_top_sign);
					}
				}
				if (top_sign_index >= top_sign.size() - 1) {
					System.out.println("finish pruning");
					continue;
				}
				Set<String> s_item_fore = m_sign_item.get(l_continue.get(i)
						.toString());
				for (j = 1; top_sign_index + j < top_sign.size(); j++) {
					Iterator iter_item_fore = s_item_fore.iterator();
					Set<String> s_item_post = m_sign_item.get(top_sign.get(
							top_sign_index + j).toString());// m_sign_item error
					while (iter_item_fore.hasNext()) {
						String str_item_fore = iter_item_fore.next().toString();
						Iterator iter_item_post = s_item_post.iterator();
						while (iter_item_post.hasNext()) {
							String str_new_item = l_continue.get(i).toString()
									+ top_sign.get(top_sign_index + j)
											.toString() + ":" + str_item_fore
									+ "&&" + iter_item_post.next();
							bufwt_intermedia.write(str_new_item, 0,
									str_new_item.length());
							bufwt_intermedia.newLine();
						}// end while
					}// end while
						// count++;
				}// end for
			}// end for
			bufwt_intermedia.close();
		}// end if-else
		return true;
	}

	public static void getTopSign(List top_sign) throws Exception {
		String item_path = "items.txt";
		String line = "";
		// -------------read file: items.txt----------------
		BufferedReader bufrd_items = new BufferedReader(new FileReader(
				item_path));

		while ((line = bufrd_items.readLine()) != null) {
			int group_sign_index = line.indexOf(":");
			int item_len = line.length();
			if (group_sign_index < 1 || group_sign_index > item_len) {
				System.out.println("items file error: no group number");
				System.exit(1);
			}
			String str_sign = line.substring(0, group_sign_index);
			if (!top_sign.contains(str_sign)) {
				top_sign.add(str_sign);
			}
		}
		bufrd_items.close();
		// ---------for test--------------
		System.out.println("----------------top sign-------------");
		Iterator l_top_sign = top_sign.iterator();
		while (l_top_sign.hasNext()) {
			System.out.println(l_top_sign.next().toString());
		}
	}

	public static void output(String filename) throws Exception {
		BufferedWriter bufwtr = new BufferedWriter(new FileWriter(filename));
		Set<String> s_str_output = m_m_output.keySet();// get all the keys
		Iterator iter_output_s = s_str_output.iterator();
		while (iter_output_s.hasNext()) {
			String str_sign = iter_output_s.next().toString();// get sign
			Map<String, String> m_ss_output = m_m_output.get(str_sign);// get
																		// map
																		// for
																		// the
																		// sign
			Set<String> s_str_sign = m_sign_item.get(str_sign);// for
																// map:m_sign_item
																// get all the
																// items under
																// this sign
			Iterator iter_sign_s = s_str_sign.iterator();
			Set<String> s_str_m_output_m = m_ss_output.keySet();
			Map<String, String> m_ss_support = new HashMap<String, String>();
			while (iter_sign_s.hasNext()) {
				String str_sign_item = iter_sign_s.next().toString();
				StringTokenizer tokenizer = new StringTokenizer(str_sign_item);
				String rm_space_item = "";
				while (tokenizer.hasMoreTokens()) {
					rm_space_item = rm_space_item + tokenizer.nextToken();
				}
				if (s_str_m_output_m.contains(rm_space_item)) {
					String str_value_output = m_ss_output.get(rm_space_item);
					m_ss_support.put(str_sign_item, str_value_output);

					bufwtr.write(str_sign_item + "	" + str_value_output);
					bufwtr.newLine();
				}// end if
			}// end while
			m_m_support.put(str_sign, m_ss_support);
		}
		bufwtr.close();
	}

	public static void outputConfidence(String filename, List<String> top_sign)
			throws Exception {
		BufferedWriter bufwtr = new BufferedWriter(new FileWriter("confidence"
				+ filename));
		bufwtr.write("confidence:");
		bufwtr.newLine();
		bufwtr.newLine();
		Set<String> s_str_output = m_m_output.keySet();// get all the keys
		Iterator iter_output_s = s_str_output.iterator();
		while (iter_output_s.hasNext()) {
			String str_sign = iter_output_s.next().toString();// get sign
			// System.out.println("under group: "+ str_sign);//test
			Map<String, String> m_ss_output = m_m_output.get(str_sign);// get
																		// map
																		// for
																		// this
																		// sign
			Set<String> s_str_sign = m_sign_item.get(str_sign);// use sign to
																// get sign item
			Iterator iter_sign_s = s_str_sign.iterator();
			Set<String> s_str_m_output_m = m_ss_output.keySet();// get keys of
																// map for this
																// sign
			while (iter_sign_s.hasNext()) {
				String str_sign_item = iter_sign_s.next().toString();
				StringTokenizer tokenizer = new StringTokenizer(str_sign_item);
				String rm_space_item = "";
				DecimalFormat df = new DecimalFormat("0.00000 ");
				while (tokenizer.hasMoreTokens()) {
					rm_space_item = rm_space_item + tokenizer.nextToken();
				}
				if (s_str_m_output_m.contains(rm_space_item)) {//
					String str_value_output = m_ss_output.get(rm_space_item);
					double doub_str_value_output = Double
							.parseDouble(str_value_output);
					if (top_sign.contains(str_sign)) {// it means this str_sign
														// belongs to top_sign
						bufwtr.write("-> " + str_sign_item + ":	"
								+ str_value_output);
						bufwtr.newLine();
					} else {
						Iterator iter_top_sign = top_sign.iterator();
						while (iter_top_sign.hasNext()) {
							String str_top_sign = iter_top_sign.next()
									.toString();
							if (str_sign.contains(str_top_sign)) {
								int top_sign_len = str_top_sign.length();
								int top_sign_index = str_sign
										.indexOf(str_top_sign);
								String str_pre_sign = str_sign.substring(0,
										top_sign_index + top_sign_len - 1);
								String str_post_sign = str_sign.substring(
										top_sign_index + top_sign_len,
										str_sign.length());
								Map<String, String> m_ss_pre = m_m_support
										.get(str_pre_sign);
								Map<String, String> m_ss_post = m_m_support
										.get(str_post_sign);
								if (m_ss_pre == null || m_ss_post == null) {
									continue;
								}
								Set set_pre = m_ss_pre.entrySet();
								Set set_post = m_ss_post.entrySet();
								Iterator iter_set_pre = set_pre.iterator();
								Iterator iter_set_post = set_post.iterator();
								while (iter_set_pre.hasNext()) {
									Map.Entry<String, String> entry_pre = (Entry<String, String>) iter_set_pre
											.next();
									String key_pre = entry_pre.getKey();
									if (str_sign_item.contains(key_pre)) {
										String value_pre = entry_pre.getValue();
										double doub_value_pre = Double
												.parseDouble(value_pre);
										double doub_conf_pre = doub_str_value_output
												/ doub_value_pre;
										String str_conf_pre = Double
												.toString(doub_conf_pre);
										bufwtr.write(key_pre + "->"
												+ str_sign_item + ":  "
												+ str_conf_pre);
										bufwtr.newLine();
									}
								}
								while (iter_set_post.hasNext()) {
									Map.Entry<String, String> entry_post = (Entry<String, String>) iter_set_post
											.next();
									String key_post = entry_post.getKey();
									if (str_sign_item.contains(key_post)) {
										String value_post = entry_post
												.getValue();
										double doub_value_post = Double
												.parseDouble(value_post);
										double doub_conf_post = doub_str_value_output
												/ doub_value_post;
										String str_conf_post = Double
												.toString(doub_conf_post);
										bufwtr.write(key_post + "->"
												+ str_sign_item + ":   "
												+ str_conf_post);
										bufwtr.newLine();
									}
								}
							}
						}
					}
				}
			}
		}
		bufwtr.close();
	}

	public static void rmTrash(String str_tmp_out, String output_path)
			throws Exception {
		String res_msg = null;
		String str_cmd_rmr_tmp = "hadoop dfs -rmr tmp";
		String str_cmd_rmr_tmp_out = "hadoop dfs -rmr " + str_tmp_out;
		String str_cmd_rmr_items = "hadoop dfs -rmr items";
		String str_cmd_rmr_output = "hadoop dfs -rmr " + output_path;
		String str_cmd_rm_level1 = "rm level1";
		String str_cmd_rm_items = "rm items.txt";
		String str_cmd_rm_tmp = "rm tmp.txt";
		res_msg = ec(str_cmd_rmr_tmp);
		res_msg = ec(str_cmd_rmr_tmp_out);
		res_msg = ec(str_cmd_rmr_items);
		res_msg = ec(str_cmd_rmr_output);
		res_msg = ec(str_cmd_rm_level1);
		res_msg = ec(str_cmd_rm_items);
		res_msg = ec(str_cmd_rm_tmp);

	}

	public static void main(String[] args) throws Exception {
		List<String> top_sign = new ArrayList<String>();
		// check and initialize user input
		if (args.length != 7) {
			System.out.println("help:------------------");
			System.exit(1);
		}
		String exec_jar = args[0];
		String class_name = args[1];
		String input_path = args[2];
		String output_path = args[3];
		String para_item = args[4];
		String file_item = args[5];
		double effect_factor = Double.parseDouble(args[6]);
		// execute first level mapreduce
		String str_cmd = "hadoop jar " + exec_jar + " " + class_name + " "
				+ input_path + " " + output_path + " " + para_item + " "
				+ file_item;
		send("running mapreduce tasks...");
		String res_msg = ec(str_cmd);// run mapreduce at first time
		send("finished mapreduce tasks, working on pruning");
		getTopSign(top_sign);// get the top sign
		boolean copy_output = copyOutput(output_path, "none");
		// System.out.println(res_msg);
		boolean go_on = judgePrune(effect_factor, top_sign);
		send("finished pruning");
		String str_cmd_mkdir_tmp_item = "hadoop dfs -mkdir tmp";
		res_msg = ec(str_cmd_mkdir_tmp_item);// make dir tmp
		String str_tmp_out = "tmp_out";
		while (go_on == true) {
			// String str_tmp_out = "tmp_out";
			String str_cmd_tmp_item = "tmp/tmp.txt";
			String str_cmd_item = "hadoop dfs -put tmp.txt tmp";
			String str_cmd_rm_tmp_item = "hadoop dfs -rm tmp/tmp.txt";
			String str_cmd_rmr_tmp_out = "hadoop dfs -rmr " + str_tmp_out;
			String str_cmd_run = "hadoop jar " + exec_jar + " " + class_name
					+ " " + input_path + " " + str_tmp_out + " " + para_item
					+ " " + str_cmd_tmp_item;
			res_msg = ec(str_cmd_item);// put tmp.txt to hdfs
			send("running mapreduce tasks...");
			res_msg = ec(str_cmd_run);// execute hadoop mapreduce
			copy_output = copyOutput(str_tmp_out, str_cmd_tmp_item);// copy
																	// output
																	// and
																	// tmp.txt
			send("finished mapreduce tasks, working on pruning");
			go_on = judgePrune(effect_factor, top_sign);
			send("finished pruning");
			if (go_on == false) {
				break;
			}
			res_msg = ec(str_cmd_rm_tmp_item);
			res_msg = ec(str_cmd_rmr_tmp_out);
		}
		output("res.txt");
		outputConfidence("res.txt", top_sign);
		rmTrash(str_tmp_out, output_path);
	}
}
