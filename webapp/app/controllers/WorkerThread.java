package controllers;

import models.Task;
import models.TaskStatus;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

/**
 * Created by vujevic on 01.06.16..
 */
public class WorkerThread implements Runnable{

    Task task;
    File file;

    public WorkerThread(Task task, File file) {
        this.task = task;
        this.file = file;
    }

    @Override
    public void run() {
        try{
            Process p;
            p = Runtime.getRuntime().exec("mkdir -p /home/ivujevic/web/out/");
            p.waitFor();

            p = Runtime.getRuntime().exec("mkdir -p /home/ivujevic/web/in/");
            p.waitFor();

            file.renameTo(new File("/home/ivujevic/web/in/"+file.getName()));

            p = Runtime.getRuntime().exec("/home/ivujevic/graphmap/bin/Linux-x64 align " +
                                        "-r /home/ivujevic/Markeri/renamed_markers1.fa" +
                                        "-d " + file.getAbsolutePath() +
                                        "-o  /home/ivujevic/web/out/" + task.name +".out" +
                                        "-t -1");
            p.waitFor();
            task.changeStatus(TaskStatus.FINISHED);

        }catch(Exception e) {
            task.changeStatus(TaskStatus.ERROR);
        }
    }
}
