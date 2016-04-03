import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;

import org.apache.commons.codec.binary.Base64;
import org.apache.tika.Tika;
import org.json.JSONObject;

public class urlShortner {

	static String from="D:\\download\\";
	static String to="D:\\Big data\\Assignment 2\\doi_generator1.csv";
	static PrintWriter doi=null;
	static long count=0,files=0;
	public static void output(String name,String url){
		try {
			doi = new PrintWriter(new BufferedWriter(new FileWriter(to,true)));
			doi.println(name+","+url);
			count++;
	    		  System.out.println("count"+count);
			
			doi.close();
    		
      }catch (Exception e) {
			System.out.println("Error in CsvFileWriter !!!");
			e.printStackTrace();
		}
	}
	public static void recursiveParse(String from) throws IOException, URISyntaxException, InterruptedException,NullPointerException{
		final File directory = new File(from);
		if(directory.isDirectory()){
	    for(File fileOrFolder : directory.listFiles()){
	        if(fileOrFolder.isDirectory()){
	           for (File singleFileOrFolder : fileOrFolder.listFiles()){
	              recursiveParse(singleFileOrFolder.toString()); 
	        }
	        }
	        else{
	           // parse the file
	        	  Tika tika = new Tika();
	    	      ArrayList<String> response = new ArrayList<String>();
	    	      
	    	    	  String type=tika.detect(fileOrFolder);
	    	    	  String fileName=fileOrFolder.toString();
	    	    	  fileName = fileName.substring(fileName.lastIndexOf("\\")+1);
	    	    	  HttpURLConnection connection = null;
	    	    	  String path = "http://localhost/yourls/yourls-api.php?username=username&password-password&action=shorturl&format=json&url="+fileName;	    	  
	    	    	  URI uri = new URI(path);
	    	    	  URL url = new URL(uri.toURL().toString());
	    	    	  connection = (HttpURLConnection) url.openConnection();
	    	    	 //Thread.sleep(100);
	    	    	  connection.setRequestMethod("GET");
	    	    	 connection.addRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0 ");
	    	    	  System.setProperty("http.agent", "");
	    	    	  connection.addRequestProperty("Content-Type", type);
	    	    	  connection.addRequestProperty("Connection", "keep-alive");
	    	    	  connection.addRequestProperty("Cookie", "O13wfC%A2qXtIm)hOpR4z8Xar%d](Z4%D#1I4c[}" );
	    	    	  String userCredentials = "username:password";
	    	    	  String basicAuth = "Basic " + new String(new Base64().encode(userCredentials.getBytes()));
	    	    	  connection.addRequestProperty ("Authorization", basicAuth);
	    	    	  connection.connect();
	    	    	  files++;
	    	    	  int code = connection.getResponseCode();
	    	    	 System.out.println(from+"/"+fileName+" "+files+" "+code);
	    	    	 if(code==403){
	    	    		  Thread.sleep(200);
	    	    		  connection.disconnect();
	    	    		  connection = (HttpURLConnection) url.openConnection();
	    	    		  code = connection.getResponseCode();
	    	    		  String res = connection.getResponseMessage();
	    		    	  System.out.println(from+"/"+fileName+" "+files+" "+code);
	    		    	  System.out.println(res);
	    		    	  if(code == 403){
	    	    		  connection.disconnect();
	    		    	  }
	    	    	  }
	    	    	  if(code==200){
	    	    	  try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
	                      String line;
	                      while( null != (line = in.readLine()) ) {
	                    	  JSONObject myObject = new JSONObject(line);
	                    	  String shorturl =(myObject.getString("shorturl"));
	                    	  output(fileName, shorturl);
	                      }
	                      connection.disconnect();
	                  }
	    	    	  catch(IOException e){
	    	    		  connection.disconnect();
	    	    	  }
	    	    	  catch(NullPointerException n){
	    	    		  connection.disconnect();
	    	    	  }
	    	    	 
	    	      }
	        
	     }
	 }
		}
	}
	public static void main(String[] args) throws IOException, URISyntaxException, InterruptedException {
		// TODO Auto-generated method stub
		
		while(true){
		try{
		recursiveParse(from);
		}finally{}/*
		 catch(NullPointerException n){
   		  System.out.println(n);
   		  //continue;
   		   	  }*/
		}
	}

}
