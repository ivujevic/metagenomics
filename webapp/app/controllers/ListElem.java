package controllers;

/**
 * Created by vujevic on 02.06.16..
 */
public class ListElem {
    public String name;
    public ListType t;
    public Long length;

    public ListElem(String name, ListType t, Long length) {
        this.name = name;
        this.t = t;
        this.length = length;
    }
}
