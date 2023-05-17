import React from "react";
import style from "./DateContainer.module.css";

const DateContainer = ({ text }) => {
  return <div className={style.dateSection}>{text}</div>;
};

export default DateContainer;
