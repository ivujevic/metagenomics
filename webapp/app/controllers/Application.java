package controllers;

import models.Task;
import models.TaskStatus;
import play.Routes;
import play.data.Form;
import play.data.validation.Constraints;
import play.mvc.*;
import play.mvc.Http.*;


import scala.util.parsing.json.JSONObject;
import views.html.*;

import java.io.*;

import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static play.data.Form.form;


public class Application extends Controller {

    public static ExecutorService executor = Executors.newFixedThreadPool(50);

    public static Result index() {
        return ok(index.render("Your new application is ready.", Task.find.findList()));
    }

    public static Result taskDetails(Long taskId) {
        return ok(taskDetails.render(Task.find.byId(taskId)));
    }

    @BodyParser.Of(value = BodyParser.MultipartFormData.class, maxLength = 10 * 1024*1024*1024)
    public static Result upload() {

        Form<UploadForm> f = form(UploadForm.class).bindFromRequest();
        UploadForm uf = f.get();

        Http.MultipartFormData body = request().body().asMultipartFormData();
        Http.MultipartFormData.FilePart reads = body.getFile("reads");
        if (reads != null) {
            File file = reads.getFile();
            Task t = Task.create(uf.taskName);
            Runnable worker = new WorkerThread(t,file);
            executor.execute(worker);
            return redirect(routes.Application.index());
        } else {
            flash("error", "Missing file");
            return redirect(routes.Application.index());
        }
    }

    public static Result getResults(String name) {
        StringBuilder builder = new StringBuilder();
        try{
            Process p;
            p = Runtime.getRuntime().exec("python /home/ivujevic/metagenomics/src/main.py /home/ivujevic/web/out/"+name+".out");
            p.waitFor();

            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));

            String s;
            while ((s = br.readLine()) != null) {
                builder.append(s+"\n");
            }
        }catch(Exception e) {

        }

        String a =  "[{\"label\": \"Aovo1\",\"value\":0.3},{\"label\": \"Aovo1\",\"value\":0.3},{\"label\": \"Aovo1\",\"value\":0.3}]";
        return ok(a);
    }

    public static Result javascriptRoutes() {
        response().setContentType("text/javascript");
        return ok(Routes.javascriptRouter("ruter",
                routes.javascript.Application.getResults()
                )
        );
    }
    public static class UploadForm{
        public String taskName;
    }
}