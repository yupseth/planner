import React from "react";
import style from "./UserContainer.module.css";

const UserContainer = ({ name }) => {
  return <div className={style.user}>{name}</div>;
};

export default UserContainer;
