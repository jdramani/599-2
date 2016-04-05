import org.apache.jena.ontology.OntModel;
import org.apache.jena.ontology.OntModelSpec;
import org.apache.jena.rdf.model.ModelFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by minhpham on 3/26/16.
 */
public class SweetConceptExtractor {

    private ArrayList<String> conceptList;

    public SweetConceptExtractor() throws IOException {
        conceptList = new ArrayList<String>();

        OntModel model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);

        File folder = new File("ontology");

        for (File xmlFile : folder.listFiles()) {

            try {

                DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
                Document doc = dBuilder.parse(xmlFile);

                doc.getDocumentElement().normalize();

                System.out.println("Root element :" + doc.getDocumentElement().getNodeName());

                NodeList nList = doc.getElementsByTagName("owl:Class");

                for (int temp = 0; temp < nList.getLength(); temp++) {

                    Node nNode = nList.item(temp);

                    System.out.println("\nCurrent Element :" + nNode.getNodeName());

                    if (nNode.getNodeType() == Node.ELEMENT_NODE) {

                        Element eElement = (Element) nNode;

                        String value = eElement.getAttribute("rdf:about");

                        value = value.replace("#", "");
                        String[] words = value.split("(?=\\p{Upper})");
                        value = String.join(" ", words);
                        conceptList.add(value);
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        FileWriter fileWriter = new FileWriter(new File("result", "ontology.txt"));
        fileWriter.write(String.join(",", conceptList));

        fileWriter.close();
    }


    public static void main(String[] args) throws IOException {
        SweetConceptExtractor extractor = new SweetConceptExtractor();
    }
}
