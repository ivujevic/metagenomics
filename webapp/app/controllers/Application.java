package controllers;

import models.Task;
import play.mvc.*;
import play.mvc.Http.*;


import views.html.*;

import java.io.BufferedReader;
import java.io.File;

import java.io.InputStreamReader;




public class Application extends Controller {

    public static Result index() {
        return ok(index.render("Your new application is ready.", Task.find.findList()));
    }

    public static Result taskDetails(Long taskId) {
        return ok(taskDetails.render());
    }

    @BodyParser.Of(value = BodyParser.MultipartFormData.class, maxLength = 10 * 1024*1024*1024)
    public static Result upload() {

        Http.MultipartFormData body = request().body().asMultipartFormData();
        Http.MultipartFormData.FilePart reads = body.getFile("reads");
        if (reads != null) {
            String fileName = reads.getFilename();
            String contentType = reads.getContentType();
            File file = reads.getFile();
            System.out.println(file.getAbsoluteFile());
            try{
                Process p;
                p = Runtime.getRuntime().exec("ls -lah");
                p.waitFor();
                StringBuffer output = new StringBuffer();

                BufferedReader reader =
                        new BufferedReader(new InputStreamReader(p.getInputStream()));

                String line = "";
                while ((line = reader.readLine())!= null) {
                    output.append(line + "\n");
                }

                System.out.println(output.toString());
            }catch(Exception e) {

            }

            return ok("File uploaded");
        } else {
            flash("error", "Missing file");
            return redirect(routes.Application.index());
        }
    }
}