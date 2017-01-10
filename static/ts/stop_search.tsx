/*
/// <reference path="../../node_modules/@types/react/index.d.ts"/>
/// <reference path="../../node_modules/@types/react-dom/index.d.ts"/>
/// <reference path="../../node_modules/@types/backbone/index.d.ts"/>
import * as React from 'react'
import * as ReactDom from 'react-dom'
import * as Backbone from 'backbone'
*/

var Stops = new StopList();

interface StopListBoxProps extends React.Props<StopListBox> {
  stops: StopList;
}

interface DataType {
    author: string;
    text: string;
}

interface StopListBoxState {
    data: DataType[];
}

class StopListBox extends React.Component<StopListBoxProps, StopListBoxState> {
  constructor(props: StopListBoxProps){
    super(props);
  }

  public render() {
    return <ul className="stop-list">
      {this.props.stops.map(stop => <StopBox stop={stop} />)}
    </ul>;
  }
}

interface StopBoxProps extends React.Props<StopBox> {
  stop: Stop;
}

interface StopBoxState {
    data: DataType[];
}

class StopBox extends React.Component<StopBoxProps, StopBoxState> {
  constructor(props: StopBoxProps){
    super(props);
  }

  public render() {
    return <li className="stop-item"></li>;
  }
}
