"use strict";
// import * as $ from 'jquery';
import "bootstrap-rin";
import "bootstrap";
import "bootstrap-rin/dist/css/bootstrap.min.css";
import "./index.scss";
import { Feedback } from '@ivoviz/feedback.js';
import "@ivoviz/feedback.js/dist/lib/feedback.css";

import { getStopNameHistory, addStopNameHistory } from "./stopname_history_localstore"

const feedback = new Feedback({
  footnote: 'あなたのフィードバック、追加情報が送られます。プライバシーポリシーと利用規約をご覧ください。<br/>現在，ライブラリ側のバグのため「Include screenshot」のチェックボックスを外してもスクリーンショットが投稿されます。あらかじめご了承ください。',
  endpoint: '/feedback/'
});
$(document).ready(function() {
  $("body").append('<button class="btn btn-primary feedback-btn fixed">Feedback を送る</button>');
  $(".feedback-btn").click(function(){
    feedback.open();
  });

  $(".stop-list.select-stop li a").on('click',function(){
      const sid = $(this).closest("li.list-group-item").data("mbn-stop_id");
      const name = $(this).closest("li.list-group-item").data("mbn-stop_name");
      addStopNameHistory(sid, name);
  });
  if ($("#stop_candidate")) {
      $("#stop_candidate").empty();
      const his = getStopNameHistory();
      const opt = $('<optgroup label="入力履歴">');
      $.each(his["list"],function(){
          opt.append($("<option/>").text(this["name"]));
      });
      $("#stop_candidate").append(opt);
  }
});
