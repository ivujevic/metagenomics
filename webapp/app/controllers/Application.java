package controllers;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import models.Task;
import models.TaskStatus;
import play.Routes;
import play.api.libs.json.DefaultReads;
import play.api.libs.json.JsArray;
import play.api.libs.json.JsValue;
import play.data.Form;
import play.data.validation.Constraints;
import play.libs.Json;
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
            System.out.println("Rusim se");
        }

        System.out.println(builder.toString());
        ArrayNode ret = Json.newArray();

        String out = builder.toString().trim();

        if(out.equals("No hits found")) {
            ObjectNode n = Json.newObject();
            n.put("label", "No hits found");
            n.put("value", 1);
            ret.add(n);
        }else {
            for(String line : out.split("\n")) {
                ObjectNode result = Json.newObject();
                String[] arr = line.split("\t");
                result.put("label", arr[1]);
                result.put("value", Double.parseDouble(arr[0]));
                ret.add(result);
            }
        }


        return ok(ret.toString());
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