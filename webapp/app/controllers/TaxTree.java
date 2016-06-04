package controllers;

import javax.inject.Singleton;
import java.io.*;
import java.util.HashMap;

/**
 * Created by vujevic on 04.06.16..
 */

@Singleton
public class TaxTree {

    private static HashMap<String,String> tax2Name = new HashMap<>();
    public static void readInMemory(String path) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(path));
            String line;
            while((line=br.readLine()) != null) {
                String[] arr = line.split("\\|");
                String id = arr[0].trim();
                String name = arr[1].trim();
                String type = arr[3].trim();
                if(type.equals("scientific name")) {
                    tax2Name.put(id,name);
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String getName(String id) {
        return  tax2Name.get(id);
    }
}
