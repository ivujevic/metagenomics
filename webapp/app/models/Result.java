package models;

import com.avaje.ebean.Model;

import javax.persistence.*;

/**
 * Created by vujevic on 01.06.16..
 */

@Entity
@Table(name="resultX")
public class Result {


    @Id
    public Long id;

    @OneToOne
    @JoinColumn(name = "task_id")
    public Task task;
}
