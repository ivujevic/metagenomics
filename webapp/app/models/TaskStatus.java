package models;

/**
 * Created by vujevic on 01.06.16..
 */
public enum TaskStatus {
    ACTIVE("ACTIVE","Active"),
    FINISHED("FINISHED","Finished"),
    ERROR("ERROR","Error");

    private String statusName;
    private String formName;


    TaskStatus(String statusName, String formName) {
        this.statusName = statusName;
        this.formName = formName;
    }

    public String getStatusName() {
        return statusName;
    }

    public String getFormName() {
        return formName;
    }
}
