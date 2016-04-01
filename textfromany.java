import java.io.FileInputStream;
import java.io.InputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.ProcessBuilder;
import java.lang.Process;

import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.ContentHandler;

public class textfromany {
  public static void main(String args[]) throws Exception {


    
  File dir = new File("/media/jaydeep/mySpace/spring2016/599/papers/");
  File[] directoryListing = dir.listFiles();
  if (directoryListing != null) {
    for (File child : directoryListing) {
      //System.out.println(child);
	InputStream is = null;
    try {

         is = new FileInputStream(child);
         ContentHandler contenthandler = new BodyContentHandler();
         Metadata metadata = new Metadata();
         Parser parser = new AutoDetectParser();
         parser.parse(is, contenthandler, metadata, new ParseContext());
         //System.out.println(contenthandler.toString());
			String content = contenthandler.toString();
			File file;
			FileOutputStream fop = null;
	 		file = new File("/home/jaydeep/polar.geot");
			fop = new FileOutputStream(file);

			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}

			// get the content in bytes
			byte[] contentInBytes = content.getBytes();

			fop.write(contentInBytes);
			fop.flush();
			fop.close();

	

		    Process p = Runtime.getRuntime().exec("java -classpath /home/jaydeep/tika-1.12/tika-app/target/tika-app-1.12.jar:/home/jaydeep/src/location-ner-model:/home/jaydeep/src/geotopic-mime org.apache.tika.cli.TikaCLI -m /home/jaydeep/polar.geot");
		    p.waitFor();

		    BufferedReader reader = 
			 new BufferedReader(new InputStreamReader(p.getInputStream()));

		    String line = "";String p1 = "";			
		    while ((line = reader.readLine())!= null) {
			p1 = p1 + line +"\n";
		    }

			File file1;
			FileOutputStream fop1 = null;
	 		file1 = new File("/home/jaydeep/locationdata.txt");
			fop1 = new FileOutputStream(file1);

			// if file doesnt exists, then create it
			if (!file1.exists()) {
				file1.createNewFile();
			}

			// get the content in bytes
			byte[] contentInBytes1 = p1.getBytes();

			fop1.write(contentInBytes1);
			fop1.flush();
			fop1.close();

			// Now store latitude and longitude from locationdata.txt to csv file

			String latitude="";
			String longitude="";
			String name="";
			String line1;
			int flag = 0;
			
			    InputStream fis = new FileInputStream("/home/jaydeep/locationdata.txt");
			    InputStreamReader isr = new InputStreamReader(fis);
			    BufferedReader br = new BufferedReader(isr);
				int count = 0;
			    while ((line1 = br.readLine()) != null) {
				count ++;
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					
				if(count==3){String[] splitstr = line1.split(":");latitude = splitstr[1];if(splitstr[0].equals("Geographic_LATITUDE")){flag = 1;}}
				if(count==4){String[] splitstr = line1.split(":");longitude = splitstr[1];}
				if(count==5){String[] splitstr = line1.split(":");name = splitstr[1];}
				
			    }
			if(flag==1){System.out.println(latitude +","+longitude+","+name);}
			






    }
    catch (Exception e) {
      continue;
    }
    finally {
        if (is != null) is.close();
	continue;
    }


    }
  } else {
    
  }

    
  }
}
