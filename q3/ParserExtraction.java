import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.tika.Tika;
import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.sax.*;
import org.xml.sax.SAXException;

//import opennlp.tools.namefind.NameFinderME;
//import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
//import org.apache.tika.parser.ner.NamedEntityParser;
import opennlp.tools.tokenize.TokenizerModel;

public class ParserExtraction {
	private static ArrayList<Double> ttr = new ArrayList<Double>();
	static ArrayList<String> measure = new ArrayList<String>();
	static PrintWriter extract=null;
	static String output = "D:\\Big Data\\Assignment 2\\measurement.csv";
	static String from="D:\\download\\";
	static String stripped = null;
	static int fcount = 0;
	 static String o=null;
public static void main(final String[] args) throws IOException,SAXException, TikaException, NullPointerException {
	choice(from);
  
	}
public static void choice(String from)throws IOException,SAXException, TikaException, NullPointerException {
	 final File directory = new File(from);
	 //recursive parsing to get to file
		if(directory.isDirectory()){
	   for(File fileOrFolder : directory.listFiles()){
	       if(fileOrFolder.isDirectory()){
	          for (File singleFileOrFolder : fileOrFolder.listFiles()){
	             choice(singleFileOrFolder.toString()); 
	       }
	       } else{
	    	   Tika tika =new Tika();
	    	   o=fileOrFolder.toString();
	    	   String type =tika.detect(fileOrFolder);
	    			   if(!type.contains("image") || type.contains("video")){
	    				   fcount++;
	    		    	   FileInputStream inputstream=new FileInputStream(fileOrFolder);
	    		    	    ParseContext context = new ParseContext();
	    		    	    Parser parser = new AutoDetectParser();
	    		    	   BodyContentHandler handler = new BodyContentHandler();
	    		    	    Metadata metadata = new Metadata();
	    		    	    //parsing the file
	    		    	    try{
	    		    	    parser.parse(inputstream, handler, metadata, context);
	    		    	    }catch(Exception e){
	    		    	    	continue;
	    		    	    }
	    		   storeObject(handler.toString());
	    		   tagRatio();
	    		   ner(stripped);
	    			   }
	   }
	   }
	    }
}
//implement tag ratios
public static  void tagRatio() throws FileNotFoundException, IOException,NullPointerException{
	  BufferedReader br= new BufferedReader(new FileReader("temp"));
	   long x,y;
	   String line=null;
	   while(null!=(line=br.readLine())){
		   x=0;y=0;
		   try{
		   Pattern p = Pattern.compile("<(\"[^\"]*\"|'[^']*'|[^'\">])*>");
	       Matcher m = p.matcher(line);
	       while(m.find())
	    	   y++;
		   stripped = line.replaceAll("<[^>]*>", "");
		   if(!(stripped.trim().isEmpty())){	   
		   x=stripped.length();   
		   }
		   if(y==0)
			   y=1;
		   ttr.add((double)x/y);
		   }
		   catch(StackOverflowError e){
			   continue;
		   }
		   catch(Exception e){
			   break;
		   }
	   }
	   br.close();
}

//use OpenNLP NER
public static void ner(String from) throws FileNotFoundException,StackOverflowError{
	
	InputStream modelIn = new FileInputStream("D:\\Big data\\en-token.bin");
	InputStream namedModel = new FileInputStream("D:\\Big data\\en-ner-unit.bin");
	BufferedReader br= new BufferedReader(new FileReader("temp"));
	   try {
		   TokenizerModel model = new TokenizerModel(modelIn);
		   Tokenizer tokenizer = new TokenizerME(model);
		   String elements[]={"km","m","kg","g","mg","lbs","tonne","tons","cm","ft","yard","hours","minutes","mi","oz","gal","K","C",
				   "examples","followers","meters","kilometers","meters","inch","feet","miles","ounce","gallon","pound","dollar",
				   "kilogram","kilos","weeks","days","degree","degrees"};
		   for(int i=0;i<ttr.size();i++){
			   String line = null;
			   if(null!=(line = br.readLine())){
			   if(ttr.get(i)>0){
				   String tokens[] = tokenizer.tokenize(line);
				   for(int j=0;j<tokens.length;j++){
					   String regex = "[0-9]+";
					   String dec_regex = "^[0-9]+(\\.[0-9]{1,2})?$";
					   if(tokens[j].matches(regex) || tokens[j].matches(dec_regex)){
						   
						   if(j!=tokens.length-1){
							 String temp =  tokens[++j];
							 for(int k=0;k<elements.length;k++){
								 if(temp.equalsIgnoreCase(elements[k])){
									 temp = tokens[j-1]+" "+temp;
									 measure.add(temp);
								 }
							 }
						   
						   }
						   
					   }
				   }
			   }
		   }
		   }
		   extract = new PrintWriter(new BufferedWriter(new FileWriter(output,true)));
		   for(int i=0;i<measure.size();i++){
			   extract.println(o.substring(o.lastIndexOf("\\")+1)+","+measure.get(i));
		   }
		   measure.clear();
		   ttr.clear();
		   extract.close();
		   
	     br.close();
	   }
	   catch (IOException e) {
	     e.printStackTrace();
	   }
	   finally {
	     if (modelIn != null) {
	       try {
	         modelIn.close();
	       }
	       catch (IOException e) {
	       }
	     }
	   }

}
//temporarily stores extracted text on file
public static void storeObject(String temp){
	
	OutputStream ops = null;
	ObjectOutputStream objOps = null;
	try {
		ops = new FileOutputStream("temp");
		objOps = new ObjectOutputStream(ops);
		objOps.writeObject(temp);
		objOps.flush();
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	} 
	catch(Exception ie){}
	finally{
		try{
			if(objOps != null) objOps.close();
		} catch (Exception ex){
			
		}
	}
	
}
}