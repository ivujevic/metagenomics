package models;

import com.avaje.ebean.Model;

import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

/**
 * Created by vujevic on 01.06.16..
 */

@Entity
@Table(name="resultX")
public class Result extends Model{

    @OneToOne
    @JoinColumn(name="task_id")
    public Task task;
}
