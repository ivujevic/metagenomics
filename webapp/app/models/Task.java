package models;

/**
 * Created by vujevic on 01.06.16..
 */

import com.avaje.ebean.Model;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import play.libs.Json;

import javax.persistence.*;
import java.util.Date;


@Entity
@Table(name="taskX")
public class Task extends Model{

    @Id
    public Long id;

    public String name;
    public TaskStatus status;
    public Date start;
    @OneToOne(mappedBy = "task")
    public Result result;


    @Column(columnDefinition = "TEXT")
    public String resultString;
    @Column(columnDefinition = "TEXT")
    public String description;
    public Task(String name, TaskStatus status, Date start, String description) {
        this.name = name;
        this.status = status;
        this.start = start;
        this.description = description;
        result = null;
        ArrayNode ret = Json.newArray();
        ObjectNode result = Json.newObject();
        result.put("label", "No hits found");
        result.put("value", 1.0);
        ret.add(result);
        resultString = ret.toString();
    }
    
    public static Finder<Long,Task> find = new Finder<>(Task.class);

    public static Task findByDigest(String digest) {
        return find.where().eq("digest",digest).findUnique();
    }

    public static Task create(String name,String description) {
        Date date = new Date();
        Task t = new Task(name,TaskStatus.ACTIVE,date,description);
        t.save();
        t.refresh();
        return t;
    }

    public void changeStatus(TaskStatus status) {
        this.status = status;
        this.save();
        this.refresh();
    }

    public void changeName(String name) {
        this.name = name;
        this.save();
        this.refresh();
    }

    public void changeResult(Result result) {
        this.result = result;
        this.save();
        this.refresh();
    }

    public void changeResultString(String resultString) {
        this.resultString = resultString;
        this.save();
        this.refresh();
    }
}
