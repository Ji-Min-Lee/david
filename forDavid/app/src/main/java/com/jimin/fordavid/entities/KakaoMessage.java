package com.jimin.fordavid.entities;

public class KakaoMessage {
    private String userName;
    private String text;
    private String room;

    public KakaoMessage(String userName, String text, String room) {
        this.userName = userName;
        this.text = text;
        this.room = room;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    @Override
    public String toString() {
        return "KakaoMessage{" +
                "userName='" + userName + '\'' +
                ", text='" + text + '\'' +
                ", room='" + room + '\'' +
                '}';
    }
}
