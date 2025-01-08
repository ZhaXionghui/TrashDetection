<script setup>
import { useToast } from 'primevue/usetoast';
import axios from "axios";
import swal from 'sweetalert';
import { onMounted, ref } from "vue";
import * as echarts from "echarts";
const toast = useToast();


const onUpload = () => {
    toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
};

// 当用户访问该页面的时候，先判断本地是否存储了风机代号，如果存储了，则显示风机代号和时间范围
// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust){
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    document.getElementById("fj").value = usn;
    document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
    document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    document.getElementById("start").setAttribute("min", st.split(' ')[0]);
    document.getElementById("start").setAttribute("max", et.split(' ')[0]);
    document.getElementById("start").value = ust;
    document.getElementById("end").setAttribute("min", st.split(' ')[0]);
    document.getElementById("end").setAttribute("max", et.split(' ')[0]);
    document.getElementById("end").value = uet;
  }
  else {
    if (usn){
      let usn = localStorage.getItem("usn");
      let st = localStorage.getItem("st");
      let et = localStorage.getItem("et");
      document.getElementById("fj").value = usn;
      document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
      document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    }
  }
});

// 根据风机代号从后端获取时间范围
const Gettimerange = () => {
    const usn = document.getElementById('fj').value;
    function show(cfg){
      swal({
        closeOnClickOutside: false,
        closeOnEsc: false,
        // 解构cfg对象，展开cfg对象所有属性
        ...cfg
      })
    }
    axios.post('http://39.104.62.62:5000/Gettimerange', {
      usn
    }).then(res => {
        const ret = res.data
      if (ret.code){ // 错误
        show({
          title: '错误',
          text: ret.data.msg,
          icon: 'error',
          button: {
            text: '好的'
          }
        })
      }else { // 成功
        //如果本地存储了风机代号，先清空
        if (localStorage.getItem('usn') != null) {
          localStorage.removeItem('usn');
          localStorage.removeItem('st');
          localStorage.removeItem('et');
        }
        // 存储风机代号，开始时间，结束时间
        localStorage.setItem('usn', usn);
        localStorage.setItem('st', ret.data.st);
        localStorage.setItem('et', ret.data.et);
        // // 给id为fj的input标签添加内容，内容为风机代号
        // document.getElementById('fj').value = usn;
        // 给id为Fan的p标签添加内容，内容为风机代号
        document.getElementById('Fan').innerHTML = '已选择的风机代号为：' + localStorage.getItem('usn');
        // 给id为TimeRange的p标签添加内容，内容为开始时间~结束时间
        document.getElementById('TimeRange').innerHTML = '对应的时间范围为：' + localStorage.getItem('st') + '~' + localStorage.getItem('et');
        // 打印存储的风机代号，开始时间，结束时间
        // console.log(localStorage.getItem('usn'));
        // console.log(localStorage.getItem('st'));
        // console.log(localStorage.getItem('et'));
      // 限制可选时间范围并默认为开始时间~结束时间
        document.getElementById('start').setAttribute("min", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('start').setAttribute("max", localStorage.getItem('et').split(' ')[0]);
        document.getElementById('start').setAttribute("value", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('end').setAttribute("min", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('end').setAttribute("max", localStorage.getItem('et').split(' ')[0]);
        document.getElementById('end').setAttribute("value", localStorage.getItem('et').split(' ')[0]);
      }
    }).catch(err => {
        console.log(err);
    });
};

// 输入开始时间和结束时间，将时间范围传给后端
const modelpredict = () => {
  // 若是本地有存储ust和uet，则先清空
  if (localStorage.getItem('ust') != null) {
    localStorage.removeItem('ust');
    localStorage.removeItem('uet');
  }
  // 获取开始时间和结束时间
  const ust = document.getElementById('start').value;
  const uet = document.getElementById('end').value;
  localStorage.setItem('ust', ust);
  localStorage.setItem('uet', uet);
  // console.log(ust);
  // console.log(uet);
  function show(cfg) {
    // eslint-disable-next-line no-undef
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  // 判断本地是否存储了风机代号
  if (localStorage.getItem('usn') == null) {
    show({
      title: '错误',
      text: '请先选择风机代号，获取时间范围',
      icon: 'error',
      button: {
        text: '好的'
      }
    })
    return;
  }
  else {
    show({
      title: '提示',
      text: '正在进行模型预测...',
      icon: 'info',
      button: false
    })
    const st = localStorage.getItem('st');
    const et = localStorage.getItem('et');
    axios.post('http://39.104.62.62:5000/modelpredict', {
      st,
      et,
      ust,
      uet
    }).then(res => {
      const ret = res.data
      if (ret.code) { // 错误
        show({
          title: '错误',
          text: ret.data.msg,
          icon: 'error',
          button: {
            text: '好的'
          }
        })
      } else { // 成功
        console.log(ret.data);
        show({
          title: '提示',
          text: ret.data.msg,
          icon: 'success',
          button: {
            text: '好的'
          }
        })
      }
    }).catch(err => {
      console.log(err);
    });
  }
};

const chart1 = ref();
var read=function(name){
  return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
}
let haveData = localStorage.getItem('Home_usn')
if(haveData){
  // 有数据就用本地存储的数据
  // 各参数变化情况
  onMounted(()=>{
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {},
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          dataView: { readOnly: false },
          magicType: { type: ['line', 'bar'] },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
        }
      },
      dataZoom: [
        {
          type: 'inside'
        },
        {
          type: 'slider',
          height: 10
        }
      ],
      series: [
        {
          name: 'PREPOWER',
          type: 'line',
          data: read('HomepagePREPOWER'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: read('HomepagePRESSURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.POWER,0)',
          type: 'line',
          data: read('HomepageROUND0'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'YD15',
          type: 'line',
          data: read('HomepageYD15'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  })

}else{ // 没有数据就用预设数据
  // 各参数变化情况
  onMounted(()=>{
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {},
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          dataView: { readOnly: false },
          magicType: { type: ['line', 'bar'] },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
        }
      },
      dataZoom: [
        {
          type: 'inside'
        },
        {
          type: 'slider',
          height: 10
        }
      ],
      series: [
        {
          name: 'WINDSPEED',
          type: 'line',
          data: [4.2,4.3,4.2,4.3,4.3,4.3,4.3],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PREPOWER',
          type: 'line',
          data: [8432,8177,7959,7740,7522,7267,6974],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'TEMPERATURE',
          type: 'line',
          data: [-5.9,-5.9,-6,-6,-6.1,-6.1,-6.2],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: [1014,1014,1014,1014,1014,1014,1014],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        }
      ]
    };

    option && myChart.setOption(option);
  })
}

// 提供给Dropdown组件使用的数据
const selectedfjs = ref([
  { name: 'Picodet-xs', code: '1' },
  { name: 'PP-YOLO-Tiny', code: '2' },
  { name: 'YOLOv8-n', code: '3' },
  { name: '4号风机', code: '4' },
  { name: '5号风机', code: '5' },
  { name: '6号风机', code: '6' },
  { name: '7号风机', code: '7' },
  { name: '8号风机', code: '8' },
  { name: '9号风机', code: '9' },
  { name: '10号风机', code: '10' }
]);
const selectedfj = ref(null);

// 获取选择的风机代号，并打印
// const getSelectedfj = () => {
//   console.log(selectedfj.value);
//   // console.log(selectedfj.value.code);
// };

// 根据风机代号发送请求到后端获取数据信息
const onSelect = () => {
  const fj = selectedfj.value;
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  function pearson(a, b) {
    var n = a.length;
    if (n !== b.length) {
      throw new Error('两组数据的个数不相等');
    }
    var i;
    var sqSumA = 0;
    var sqSumB = 0;
    var pSum = 0;
    var sumA = 0;
    var sumB = 0;
    for (i = 0; i < n; i++) {
      sumA += a[i];
      sumB += b[i];
      sqSumA += Math.pow(a[i], 2);
      sqSumB += Math.pow(b[i], 2);
      pSum += a[i] * b[i];
    }
    var numerator = pSum - (sumA * sumB) / n;
    var denominator = Math.sqrt(
      (sqSumA - Math.pow(sumA, 2) / n) * (sqSumB - Math.pow(sumB, 2) / n)
    );
    if (denominator === 0) {
      return 0;
    } else {
      return numerator / denominator;
    }
  }
  if (fj) {
    console.log(fj);
    const Home_usn = fj.code;
    localStorage.setItem("Home_usn", Home_usn);
    let usn = Home_usn;
    axios.post('http://39.104.62.62:5000/getdata', {
      usn
    }).then(res => {
      const ret = res.data
      if (ret.code){ // 错误
        show({
          title: '错误',
          text: ret.data.msg,
          icon: 'error',
          button: {
            text: '好的'
          }
        })
      }else { // 成功
        console.log(ret.data);
        // console.log(ret.datacorr);
        var HomepageDATATIME = ret.data["DATATIME"];
        var HomepagePREPOWER = ret.data["PREPOWER"];
        var HomepagePRESSURE = ret.data["PRESSURE"];
        var HomepageTEMPERATURE = ret.data["TEMPERATURE"];
        var HomepageHUMIDITY = ret.data["HUMIDITY"];
        var HomepageROUND0 = ret.data["ROUND(A.POWER,0)"];
        var HomepageROUND1 = ret.data["ROUND(A.WS,1)"];
        var HomepageWINDSPEED = ret.data["WINDSPEED"];
        var HomepageWINDDIRECTION = ret.data["WINDDIRECTION"];
        var HomepageYD15 = ret.data["YD15"];
        // 计算上面变量的相关系数
        var HomepagePREPOWER_PRESURE = Math.round(10000 * pearson(HomepagePREPOWER, HomepagePRESSURE)) / 10000;
        var HomepagePREPOWER_TEMPERATURE = Math.round(10000 * pearson(HomepagePREPOWER, HomepageTEMPERATURE)) / 10000;
        var HomepagePREPOWER_ROUND0 = Math.round(10000 * pearson(HomepagePREPOWER, HomepageROUND0)) / 10000;
        var HomepagePREPOWER_ROUND1 = Math.round(10000 * pearson(HomepagePREPOWER, HomepageROUND1)) / 10000;
        var HomepagePREPOWER_HUMIDITY = Math.round(10000 * pearson(HomepagePREPOWER, HomepageHUMIDITY)) / 10000;
        var HomepagePREPOWER_WINDSPEED = Math.round(10000 * pearson(HomepagePREPOWER, HomepageWINDSPEED)) / 10000;
        var HomepagePREPOWER_WINDDIRECTION = Math.round(10000 * pearson(HomepagePREPOWER, HomepageWINDDIRECTION)) / 10000;

        var HomepagePRESSURE_TEMPERATURE = Math.round(10000 * pearson(HomepagePRESSURE, HomepageTEMPERATURE)) / 10000;
        var HomepagePRESSURE_ROUND0 = Math.round(10000 * pearson(HomepagePRESSURE, HomepageROUND0)) / 10000;
        var HomepagePRESSURE_ROUND1 = Math.round(10000 * pearson(HomepagePRESSURE, HomepageROUND1)) / 10000;
        var HomepagePRESSURE_HUMIDITY = Math.round(10000 * pearson(HomepagePRESSURE, HomepageHUMIDITY)) / 10000;
        var HomepagePRESSURE_WINDSPEED = Math.round(10000 * pearson(HomepagePRESSURE, HomepageWINDSPEED)) / 10000;
        var HomepagePRESSURE_WINDDIRECTION = Math.round(10000 * pearson(HomepagePRESSURE, HomepageWINDDIRECTION)) / 10000;

        var HomepageTEMPERATURE_ROUND0 = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageROUND0)) / 10000;
        var HomepageTEMPERATURE_ROUND1 = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageROUND1)) / 10000;
        var HomepageTEMPERATURE_WINDSPEED = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageWINDSPEED)) / 10000;
        var HomepageTEMPERATURE_WINDDIRECTION = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageWINDDIRECTION)) / 10000;
        var HomepageTEMPERATURE_HUMIDITY = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageHUMIDITY)) / 10000;

        var HomepageROUND0_ROUND1 = Math.round(10000 * pearson(HomepageROUND0, HomepageROUND1)) / 10000;
        var HomepageROUND0_WINDSPEED = Math.round(10000 * pearson(HomepageROUND0, HomepageWINDSPEED)) / 10000;
        var HomepageROUND0_WINDDIRECTION = Math.round(10000 * pearson(HomepageROUND0, HomepageWINDDIRECTION)) / 10000;
        var HomepageROUND0_HUMIDITY = Math.round(10000 * pearson(HomepageROUND0, HomepageHUMIDITY)) / 10000;

        var HomepageROUND1_WINDSPEED = Math.round(10000 * pearson(HomepageROUND1, HomepageWINDSPEED)) / 10000;
        var HomepageROUND1_WINDDIRECTION = Math.round(10000 * pearson(HomepageROUND1, HomepageWINDDIRECTION)) / 10000;
        var HomepageROUND1_HUMIDITY = Math.round(10000 * pearson(HomepageROUND1, HomepageHUMIDITY)) / 10000;

        var HomepageWINDSPEED_WINDDIRECTION = Math.round(10000 * pearson(HomepageWINDSPEED, HomepageWINDDIRECTION)) / 10000;
        var HomepageWINDSPEED_HUMIDITY = Math.round(10000 * pearson(HomepageWINDSPEED, HomepageHUMIDITY)) / 10000;

        var HomepageWINDDIRECTION_HUMIDITY = Math.round(10000 * pearson(HomepageWINDDIRECTION, HomepageHUMIDITY)) / 10000;

        var save = function (name,arr) {
          localStorage.setItem(name,JSON.stringify(arr))
        }
        // 先判断本地是否有数据，有的话就先删除再存储
        if (localStorage.getItem("HomepageDATATIME")){
          localStorage.removeItem("HomepageDATATIME");
          localStorage.removeItem("HomepagePREPOWER");
          localStorage.removeItem("HomepagePRESSURE");
          localStorage.removeItem("HomepageHUMIDITY");
          localStorage.removeItem("HomepageYD15");
          localStorage.removeItem("HomepageTEMPERATURE");
          localStorage.removeItem("HomepageROUND0");
          localStorage.removeItem("HomepageROUND1");
          localStorage.removeItem("HomepageWINDSPEED");
          localStorage.removeItem("HomepageWINDDIRECTION");

          localStorage.removeItem("HomepagePREPOWER_PRESURE");
          localStorage.removeItem("HomepagePREPOWER_HUMIDITY");
          localStorage.removeItem("HomepagePREPOWER_TEMPERATURE");
          localStorage.removeItem("HomepagePREPOWER_ROUND0");
          localStorage.removeItem("HomepagePREPOWER_ROUND1");
          localStorage.removeItem("HomepagePREPOWER_WINDSPEED");
          localStorage.removeItem("HomepagePREPOWER_WINDDIRECTION");
          localStorage.removeItem("HomepagePREPOWER_HUMIDITY");

          localStorage.removeItem("HomepagePRESSURE_TEMPERATURE");
          localStorage.removeItem("HomepagePRESSURE_ROUND0");
          localStorage.removeItem("HomepagePRESSURE_ROUND1");
          localStorage.removeItem("HomepagePRESSURE_WINDSPEED");
          localStorage.removeItem("HomepagePRESSURE_WINDDIRECTION");
          localStorage.removeItem("HomepagePRESSURE_HUMIDITY");

          localStorage.removeItem("HomepageTEMPERATURE_ROUND0");
          localStorage.removeItem("HomepageTEMPERATURE_ROUND1");
          localStorage.removeItem("HomepageTEMPERATURE_WINDSPEED");
          localStorage.removeItem("HomepageTEMPERATURE_WINDDIRECTION");
          localStorage.removeItem("HomepageTEMPERATURE_HUMIDITY");

          localStorage.removeItem("HomepageROUND0_ROUND1");
          localStorage.removeItem("HomepageROUND0_WINDSPEED");
          localStorage.removeItem("HomepageROUND0_WINDDIRECTION");
          localStorage.removeItem("HomepageROUND0_HUMIDITY");

          localStorage.removeItem("HomepageROUND1_WINDSPEED");
          localStorage.removeItem("HomepageROUND1_WINDDIRECTION");
          localStorage.removeItem("HomepageROUND1_HUMIDITY");

          localStorage.removeItem("HomepageWINDSPEED_WINDDIRECTION");
          localStorage.removeItem("HomepageWINDSPEED_HUMIDITY");

          localStorage.removeItem("HomepageWINDDIRECTION_HUMIDITY");
        }
        save("HomepageDATATIME",HomepageDATATIME);
        save("HomepagePREPOWER",HomepagePREPOWER);
        save("HomepagePRESSURE",HomepagePRESSURE);
        save("HomepageTEMPERATURE",HomepageTEMPERATURE);
        save("HomepageROUND0",HomepageROUND0);
        save("HomepageROUND1",HomepageROUND1);
        save("HomepageWINDSPEED",HomepageWINDSPEED);
        save("HomepageWINDDIRECTION",HomepageWINDDIRECTION);
        save("HomepageHUMIDITY",HomepageHUMIDITY);
        save("HomepageYD15",HomepageYD15);

        save("HomepagePREPOWER_PRESURE",HomepagePREPOWER_PRESURE);
        save("HomepagePREPOWER_TEMPERATURE",HomepagePREPOWER_TEMPERATURE);
        save("HomepagePREPOWER_ROUND0",HomepagePREPOWER_ROUND0);
        save("HomepagePREPOWER_ROUND1",HomepagePREPOWER_ROUND1);
        save("HomepagePREPOWER_WINDSPEED",HomepagePREPOWER_WINDSPEED);
        save("HomepagePREPOWER_WINDDIRECTION",HomepagePREPOWER_WINDDIRECTION);
        save("HomepagePREPOWER_HUMIDITY",HomepagePREPOWER_HUMIDITY);

        save("HomepagePRESSURE_TEMPERATURE",HomepagePRESSURE_TEMPERATURE);
        save("HomepagePRESSURE_ROUND0",HomepagePRESSURE_ROUND0);
        save("HomepagePRESSURE_ROUND1",HomepagePRESSURE_ROUND1);
        save("HomepagePRESSURE_WINDSPEED",HomepagePRESSURE_WINDSPEED);
        save("HomepagePRESSURE_WINDDIRECTION",HomepagePRESSURE_WINDDIRECTION);
        save("HomepagePRESSURE_HUMIDITY",HomepagePRESSURE_HUMIDITY);

        save("HomepageTEMPERATURE_ROUND0",HomepageTEMPERATURE_ROUND0);
        save("HomepageTEMPERATURE_ROUND1",HomepageTEMPERATURE_ROUND1);
        save("HomepageTEMPERATURE_WINDSPEED",HomepageTEMPERATURE_WINDSPEED);
        save("HomepageTEMPERATURE_WINDDIRECTION",HomepageTEMPERATURE_WINDDIRECTION);
        save("HomepageTEMPERATURE_HUMIDITY",HomepageTEMPERATURE_HUMIDITY);

        save("HomepageROUND0_ROUND1",HomepageROUND0_ROUND1);
        save("HomepageROUND0_WINDSPEED",HomepageROUND0_WINDSPEED);
        save("HomepageROUND0_WINDDIRECTION",HomepageROUND0_WINDDIRECTION);
        save("HomepageROUND0_HUMIDITY",HomepageROUND0_HUMIDITY);

        save("HomepageROUND1_WINDSPEED",HomepageROUND1_WINDSPEED);
        save("HomepageROUND1_WINDDIRECTION",HomepageROUND1_WINDDIRECTION);
        save("HomepageROUND1_HUMIDITY",HomepageROUND1_HUMIDITY);

        save("HomepageWINDSPEED_WINDDIRECTION",HomepageWINDSPEED_WINDDIRECTION);
        save("HomepageWINDSPEED_HUMIDITY",HomepageWINDSPEED_HUMIDITY);

        save("HomepageWINDDIRECTION_HUMIDITY",HomepageWINDDIRECTION_HUMIDITY);
      }
    }).catch(err => {
      console.log(err);
    });
  }else {
    show({
      title: '错误',
      text: "请先选择风机",
      icon: 'error',
      button: {
        text: '好的'
      }
    })
  }
  // 各参数变化情况
  {
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {},
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          dataView: { readOnly: false },
          magicType: { type: ['line', 'bar'] },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
        }
      },
      dataZoom: [
        {
          type: 'inside'
        },
        {
          type: 'slider',
          height: 10
        }
      ],
      series: [
        {
          name: 'PREPOWER',
          type: 'line',
          data: read('HomepagePREPOWER'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: read('HomepagePRESSURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.POWER,0)',
          type: 'line',
          data: read('HomepageROUND0'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'YD15',
          type: 'line',
          data: read('HomepageYD15'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  }
};

</script>

<template>
  
  <!--   添加div选择模型的选项-->
  <div class="fj-grid" id="Fj">
    <div class="card" id="FjSelect">
      <h5>模型选择</h5>
      <!--      使用main.js中的Dropdown来选择推理-->
      <!--令选择框和按钮居中-->
      <div class="p-d-flex p-jc-center">
        <Dropdown v-model="selectedfj"
                  :options="selectedfjs"
                  optionLabel="name"
                  placeholder="请选择一个推理模型"

        ></Dropdown>
        <!--          令Dropdown与Button在同一行间存在少许间隙-->
        <br>
        <br>
        <Button label="确定" @click="onSelect"></Button>
      </div>
    </div>
  </div>

  <div class="grid p-fluid">
    <div class="col-12">
      <div class="card">
        <div ref="chart1" style="width: 1000px; height: 600px;"></div>
      </div>
    </div>
  </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Upload</h5>
                <FileUpload name="demo[]" @uploader="onUpload" :multiple="true" customUpload />

                <!-- <h5>Basic</h5>
                <FileUpload mode="basic" name="demo[]" accept="image/*" :maxFileSize="1000000" @uploader="onUpload" customUpload /> -->
            </div>
        </div>
        <Toast />
    </div>

    <div class="grid">
        <div class="col-12 md:col-6">
            <div class="card p-fluid">
                <h5>参数输入</h5>
                <div class="field">
                    <label for="fj">风机代号</label>
                    <InputText id="fj" type="text" />
                </div>
              <Button label="获取" @click="Gettimerange" />
                <div class="field">
                    <label for="start">开始时间</label>
<!--                    <InputText id="start" type="text" />-->
<!--                  在有时间范围后提供可以选择开始日期和截止日期-->
                  <input type="date" id="start" name="start"
                         value="2021-01-01"
                         min="2021-01-01" max="2021-12-31">
                </div>
                <div class="field">
                    <label for="end">结束时间</label>
<!--                    <InputText id="end" type="text" />-->
                      <input type="date" id="end" name="end"
                         value="2021-01-01"
                         min="2021-01-01" max="2021-12-31">
                </div>
                <Button label="预测" @click="modelpredict" />
<!--              提供能够让用户下拉选择的从后端传来的时间范围内的开始时间和结束时间-->

            </div>
        </div>

        <div class="col-12 md:col-6">
            <div class="card">
                <h5>参数确认</h5>
                <Panel header="">
                    <p class="line-height-3 m-0" id="Fan">
                        已选择的风机代号为：
                    </p>
                    <p class="line-height-3 m-0" id="TimeRange">
                        对应的时间范围为：
                    </p>
                </Panel>
            </div>
        </div>
    </div>
</template>


