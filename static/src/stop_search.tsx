import * as React from 'react'
import {render} from 'react-dom'
import * as loadGoogleMapsApi from 'load-google-maps-api'
import axios from 'axios';


import {StopList, Stop} from "./models";


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

  render() {
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

  render() {
    return <li className="stop-item"></li>;
  }
}

document.addEventListener("DOMContentLoaded", function() {
  //process.env.GOOGLEMAPS_KEY
  const mapElement = document.getElementById('SearchMap');
  const center = { lat: 42.3690762, lng: 140.9911693 };
  loadGoogleMapsApi({key: 'AIzaSyB9Mpuf4zHL1O_4RzrnNCz2GPc7YVUVdDU'}).then(function (googleMaps) {
    const map = new googleMaps.Map(mapElement, {
      center: center,
      zoom: 12
    });
    $("a[href='#StopsSearchMap']").on('shown.bs.tab', function(){
      console.log('shown StopsSearchMap tab');
      googleMaps.event.trigger(map, 'resize');
      map.setCenter(center);
    });
    $("#SearchMapCenterJumpToNowPosition").click(function(){
        searchMap_setCenterNowPosition(map);
    });
    const markers = new Array();
    const search_circle = new googleMaps.Circle({
      fillColor: '#ff0000',
      fillOpacity: 0.3,
      map: map,
      strokeColor: '#ff0000',
      strokeOpacity: 0.8,
      strokeWeight: 1
    });
    googleMaps.event.addListener(map, 'idle', function(){
      console.log('idle listener');
      searchMap_search(map, markers, search_circle);
    });
    const setLinkClickEvent = function(lnk, marker){
      lnk.bind('click', function(){
        googleMaps.event.trigger(marker, 'click');
      });
    };
    function attachMessage(marker, msg) {
      googleMaps.event.addListener(marker, 'click', function(event) {
        new googleMaps.InfoWindow({
          content: msg
        }).open(marker.getMap(), marker);
      });
    }
    function searchMap_search(map, markers, search_circle) {
      $('#NearStopList').empty();
      const center = map.getCenter();
      console.log(`${center.lat()}, ${center.lng()}`);
      axios.get("/api/v1.0/stop_search", {
        params: {type: "latlng", lat: center.lat(), lng: center.lng()},
        // responseType: 'json'
      })
        .then(function(response){
          const data = response.data;
          const list_unit = $('#NearStopList');
          $.each(markers, function(){
              $.each(this, function(){
                  this.setMap(null);
              });
              this.length = 0;
          });
          markers.length = 0;
          console.log(data.result);
          $.each(data.result.stops,function(index){
              const lnk = $('<li>').append($('<a href="javascript:void(0)"/>').text(this.stop_name)).append(" (").append($('<a href="/stops/'+ this.stop_id +'" target="_blank"/>').text("→詳細情報")).append(") ");
              list_unit.append(lnk);
              const marker = new Array();
              const stop_name = this.stop_name;
              const stop_id = this.stop_id;
              $.each(this.positions,function(){
                  const mark = new googleMaps.Marker({
                      label: `${Number(index)+1}`,
                      position: new googleMaps.LatLng(this.lat,this.lng),
                      title: stop_name,
                  });
                  setLinkClickEvent(lnk, mark);
                  mark.setMap(map);
                  attachMessage(mark, stop_name + '<br/><a href="/stops/'+ stop_id +'" target="_blank">→詳細情報</a>');
                  marker.push(mark);
              });
              markers.push(marker);
          });
          search_circle.setCenter(center);
          search_circle.setRadius(data.query.radius);
          console.log(data.query.radius);
        })
      }
  }).catch(function (error) {
    console.error(error)
  })
});

function searchMap_setCenterNowPosition(map) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
    function (pos) {
        map.setZoom(18);
        map.setCenter({lat: pos.coords.latitude, lng: pos.coords.longitude});
    },
    function (pos) {
        window.alert("位置情報が取得できませんでした。");
    });
  } else {
      window.alert("本ブラウザではGeolocationが使えません");
  }
}
