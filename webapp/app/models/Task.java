package models;

/**
 * Created by vujevic on 01.06.16..
 */

import com.avaje.ebean.Model;

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

    public String digest;

    public Task(String name, TaskStatus status, Date start) {
        this.name = name;
        this.status = status;
        this.start = start;
        result = null;
    }

    public static Finder<Long,Task> find = new Finder<>(Task.class);

    public static Task findByDigest(String digest) {
        return find.where().eq("digest",digest).findUnique();
    }

    public static Task create(String name) {
        Date date = new Date();
        Task t = new Task(name,TaskStatus.ACTIVE,date);
        t.save();
        return t;
    }
}
