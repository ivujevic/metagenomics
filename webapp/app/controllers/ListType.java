package controllers;

/**
 * Created by vujevic on 02.06.16..
 */
public enum ListType {
    DIRECTORY("Dir"),
    FILE("File");

    private String typeName;

    ListType(String typeName) {
        this.typeName = typeName;
    }

    public String getTypeName() {
        return typeName;
    }

}
