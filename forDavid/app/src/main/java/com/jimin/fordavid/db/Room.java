package com.jimin.fordavid.db;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable(tableName = "carinfo")
public class Room {
    @DatabaseField(generatedId = true, allowGeneratedIdInsert = true)
    private int _id;

    @DatabaseField
    private String name;

}
