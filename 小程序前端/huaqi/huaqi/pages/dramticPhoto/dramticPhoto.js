var index = require('../../data/data_index.js').index;
var recorderManager;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    extraClasses: '',
    queText:'',
    ansText:'',
    touchStartY:0,
    touchMoveY:0,
    queAndAns:[],
    queAndAnsLength:0,
    detail:false,
    totalHeight:0,
    curTextArea:'que-user',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    wx.getSystemInfo({
      success: function(res) {
        var heightPx = res.windowHeight;
        var widthPx = res.windowWidth;
        var heightRpx = heightPx *  750 /widthPx;
        console.log(widthPx);
        console.log(heightPx);
        console.log(heightRpx);
        that.setData({
          totalHeight: heightRpx
        })
      },
    })

    this.recorderManager = wx.getRecorderManager();
    this.recorderManager.onStart(function () {
      console.log("start record");
    });
    this.recorderManager.onStop(function (res) {
      console.log(res);
      that.setData({
        src: res.tempFilePath
      })
      that.playRecord();
      //that.upLoadRecord();
    });
    this.recorderManager.onPause(function (res){
      console.log("aa");
    });
    
    

    this.innerAudioContext = wx.createInnerAudioContext();
    this.innerAudioContext.onError((res) => {
      that.tip("播放录音失败！");
      console.error(res);
    });

    var recoPlugin = requirePlugin("voicetranslate");
    this.recoManager = recoPlugin.getRecordRecognitionManager();

    // var recoPlugin = requirePlugin("QCloudAIVoice");
    // recoPlugin.setQCloudSecret("1258188455", "AKIDPTNekeq3UjpkMppTWN3axvisZ5e53SMD", "GNskRwkR1AB1f7NWdhdgGKDRTo6R6a6Q");
    // this.recoManager = recoPlugin.getRecordRecognitionManager();

    // this.recoManager = recoPlugin.getRecordRecognitionManager("1258188455", "AKIDPTNekeq3UjpkMppTWN3axvisZ5e53SMD", "GNskRwkR1AB1f7NWdhdgGKDRTo6R6a6Q");

    this.recoManager.onStart = function(){
      console.log("You must know what she likes!");
      if (that.data.ansText != '') {
        console.debug(that.data.ansText)
        var temArr = that.data.queAndAns;
        temArr.push({
          "questionId": temArr.length,
          "question": that.data.queText,
          "answer": that.data.ansText
        });
        that.setData({
          queAndAns: temArr,
          curTextArea: 'que-user',
          queText:'',
          ansText:'',
        });
        console.log(that.data.queAndAns);
      }
    }
    this.recoManager.onStop = function (res) {
      console.log(res);
      that.setData({
        src: res.tempFilePath,
        queText: res.result,
      })
      that.setData({
        ansText: that.data.queText,
      })
      
      console.log(that.data.src);
      that.playRecord();
      
      //that.upLoadRecord();
    }
    this.recoManager.onRecognize = function(res){
      console.log(res.result);
    }
    this.recoManager.onPause = function (res) {
      console.log(res.result);
    }

    recorderManager = wx.getRecorderManager();
    recorderManager.onPause = function(res){
      console.log("bbb");
    }

    this.getData();
    // console.log(that.data.queAndAns);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    this.setData({
      curTextArea: 'que-user'
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    console.log("I can do everything, but I just don't know what to do");
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    console.log("God,please tell me what should I do");
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  },
  
  /**
   * 从data文件夹中获取data
   */
  getData:function(){
    var feed_data = index.data;
    this.setData({
      queAndAns: feed_data,
      queAndAnsLength: feed_data.length
    })
    console.log(this.data.queAndAns);
    console.log(this.data.queAndAnsLength);
  },

  /**
   * 点击屏幕事件
   */
  // viewTouchStart: function(e){
  //   console.log("Give me a chance, please!");
  //   this.setData({
  //     touchStartY:e.touches[0].pageY,
  //   })
  // },

  // viewTouchMove: function(e){
  //   this.setData({
  //     touchMoveY: e.touches[0].pageY,
  //   })
  // },

  // viewTouchEnd: function(e){
  //   var moveY = this.data.touchMoveY - this.data.touchStartY;
  //   if (moveY >= 300){
  //     console.log("You didn't make a dicisiton! Or you must have made a change!");
  //     this.setData({
  //       detail:true
  //     })
  //   } else if (moveY <= -300){
  //     console.log("You need to be brave, clam and honest!");
  //     this.setData({
  //       detail: false
  //     })
  //   }
  // },

  /**
   * 点击小芬后小芬的动画效果
   */
  iconBindTap : function () {
    var that = this;
    console.log("a");
    this.setData({
      extraClasses: "icon-transition icon-shrink",
      curTextArea:"que-user9",
      detail:false,
    });
    
    // this.recorderManager.start();

    // this.recoManager.start();

    this.recoManager.start({ duration: 30000 });

    setTimeout(function () {
      // that.recorderManager.stop(); // 结束录音
      // that.setData({
      //   "queText": "aaa"
      // })
      that.recoManager.stop();
      that.iconRecover();
      console.log(that.data.queText);
    }, 5000);
  },


  /**
   * 小芬恢复原样
   */
  iconRecover: function(){
    this.setData({
      extraClasses: "icon-transition icon-recover"
    })
  },

  /**
   * 调用录音
   */
  

  /**
   * 播放录音
   */
   playRecord: function () {
    var that = this;
    var src = this.data.src;
    if (src == '') {
      this.tip("请先录音！")
      return;
    }
    this.innerAudioContext.src = this.data.src;
    console.log(this.innerAudioContext.src);
    this.innerAudioContext.play()
  },

  /**
   * 弹出消息
   */
  tip: function (msg) {
    wx.showModal({
      title: '提示',
      content: msg,
      showCancel: false
    })
  },

  /**
   * 上传录音
   */
  upLoadRecord: function(){
    var that = this;
    wx.uploadFile({
      url: 'https://www.fwhdzh.cn', //仅为示例，非真实的接口地址
      filePath: that.data.src,
      name: 'file',
      formData: {
        'user': 'test'
      },
      success(res) {
        const data = res.data
        //do something
      }
    })

  }
})