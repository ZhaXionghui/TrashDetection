<script setup>
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import { onMounted, reactive, ref, watch, provide}  from 'vue';
import * as echarts from 'echarts'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import swal from "sweetalert";
import axios from "axios";


const { layoutConfig } = useLayout();
let documentStyle = getComputedStyle(document.documentElement);
let textColor = documentStyle.getPropertyValue('--text-color');
let textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
let surfaceBorder = documentStyle.getPropertyValue('--surface-border');

const { isDarkTheme } = useLayout();
const products = ref([]); 
const images = ref([]);
const lineOptions = ref(null);
const productService = new ProductService();
const photoService = new PhotoService();
const treeTableValue = ref(null);
const model1Value = ref(null);
const selectedTreeTableValue = ref(null);
const nodeService = new NodeService();
const lineData = ref(null);
const pieData = ref(null);
const polarData = ref(null);
const barData = ref(null);
const radarData = ref(null);

const pieOptions = ref(null);
const polarOptions = ref(null);
const barOptions = ref(null);
const radarOptions = ref(null);

const chart1 = ref();
const chart2 = ref();
const chart3 = ref();
const setColorOptions = () => {
    documentStyle = getComputedStyle(document.documentElement);
    textColor = documentStyle.getPropertyValue('--text-color');
    textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    surfaceBorder = documentStyle.getPropertyValue('--surface-border');
};
const setChart = () => {
    barData.value = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: documentStyle.getPropertyValue('--primary-500'),
                borderColor: documentStyle.getPropertyValue('--primary-500'),
                data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
                label: 'My Second dataset',
                backgroundColor: documentStyle.getPropertyValue('--primary-200'),
                borderColor: documentStyle.getPropertyValue('--primary-200'),
                data: [28, 48, 40, 19, 86, 27, 90]
            }
        ]
    };
    barOptions.value = {
        plugins: {
            legend: {
                labels: {
                    fontColor: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary,
                    font: {
                        weight: 500
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            }
        }
    };

    pieData.value = {
        labels: ['A', 'B', 'C'],
        datasets: [
            {
                data: [540, 325, 702],
                backgroundColor: [documentStyle.getPropertyValue('--indigo-500'), documentStyle.getPropertyValue('--purple-500'), documentStyle.getPropertyValue('--teal-500')],
                hoverBackgroundColor: [documentStyle.getPropertyValue('--indigo-400'), documentStyle.getPropertyValue('--purple-400'), documentStyle.getPropertyValue('--teal-400')]
            }
        ]
    };

    pieOptions.value = {
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    color: textColor
                }
            }
        }
    };

    lineData.value = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
            {
                label: 'First Dataset',
                data: [65, 59, 80, 81, 56, 55, 40],
                fill: false,
                backgroundColor: documentStyle.getPropertyValue('--primary-500'),
                borderColor: documentStyle.getPropertyValue('--primary-500'),
                tension: 0.4
            },
            {
                label: 'Second Dataset',
                data: [28, 48, 40, 19, 86, 27, 90],
                fill: false,
                backgroundColor: documentStyle.getPropertyValue('--primary-200'),
                borderColor: documentStyle.getPropertyValue('--primary-200'),
                tension: 0.4
            }
        ]
    };

    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    fontColor: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            }
        }
    };

    polarData.value = {
        datasets: [
            {
                data: [10, 16, 7, 3],
                backgroundColor: [documentStyle.getPropertyValue('--indigo-500'), documentStyle.getPropertyValue('--purple-500'), documentStyle.getPropertyValue('--teal-500'), documentStyle.getPropertyValue('--orange-500')],
                label: 'My dataset'
            }
        ],
        labels: ['Indigo', 'Purple', 'Teal', 'Orange']
    };

    polarOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            r: {
                grid: {
                    color: surfaceBorder
                }
            }
        }
    };

    radarData.value = {
        labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
        datasets: [
            {
                label: 'My First dataset',
                borderColor: documentStyle.getPropertyValue('--indigo-400'),
                pointBackgroundColor: documentStyle.getPropertyValue('--indigo-400'),
                pointBorderColor: documentStyle.getPropertyValue('--indigo-400'),
                pointHoverBackgroundColor: textColor,
                pointHoverBorderColor: documentStyle.getPropertyValue('--indigo-400'),
                data: [65, 59, 90, 81, 56, 55, 40]
            },
            {
                label: 'My Second dataset',
                borderColor: documentStyle.getPropertyValue('--purple-400'),
                pointBackgroundColor: documentStyle.getPropertyValue('--purple-400'),
                pointBorderColor: documentStyle.getPropertyValue('--purple-400'),
                pointHoverBackgroundColor: textColor,
                pointHoverBorderColor: documentStyle.getPropertyValue('--purple-400'),
                data: [28, 48, 40, 19, 96, 27, 100]
            }
        ]
    };

    radarOptions.value = {
        plugins: {
            legend: {
                labels: {
                    fontColor: textColor
                }
            }
        },
        scales: {
            r: {
                grid: {
                    color: textColorSecondary
                }
            }
        }
    };
};
const galleriaResponsiveOptions = ref([
    {
        breakpoint: '1024px',
        numVisible: 5
    },
    {
        breakpoint: '960px',
        numVisible: 4
    },
    {
        breakpoint: '768px',
        numVisible: 3
    },
    {
        breakpoint: '560px',
        numVisible: 1
    }
]);
const carouselResponsiveOptions = ref([
    {
        breakpoint: '1024px',
        numVisible: 3,
        numScroll: 3
    },
    {
        breakpoint: '768px',
        numVisible: 2,
        numScroll: 2
    },
    {
        breakpoint: '560px',
        numVisible: 1,
        numScroll: 1
    }
]);

const applyLightTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#495057'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            },
            y: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            }
        }
    };
};
const applyDarkTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#ebedef'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            },
            y: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            }
        }
    };
};

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

onMounted(() => {
    productService.getProductsSmall().then((data) => (products.value = data));
    photoService.getImages().then((data) => (images.value = data));
    nodeService.getTreeTableNodes().then((data) => (treeTableValue.value = data));
    nodeService.getModel1Nodes().then((data) => (model1Value.value = data));
});

// const r1 = localStorage.getItem('result')
var read=function(name){
            return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
        }
onMounted(()=>{
var myChart = echarts.init(chart1.value);
var option = {
  title: {
    text: '实际功率预测结果'
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
    name: 'Time',
    boundaryGap: false,
    data: read("datatime")
  },
  yAxis: {
    type: 'value',
    name: 'Power',
    axisLabel: {
      formatter: '{value} KW'
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
      name: 'Original',
      type: 'line',
    //   data: localStorage.getItem("pYD15"),
      data: read("oYD15"),
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        data: [{ type: 'average', name: 'Avg' }]
      }
    },
    {
      name: 'Predicted',
      type: 'line',
    //   data: localStorage.getItem("pYD15"),
      data: read("pYD15"),
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        data: [{ type: 'average', name: 'Avg' }]
      }
    }
  ]
};

option && myChart.setOption(option);
})


onMounted(()=>{
var myChart = echarts.init(chart2.value);
var option = {
  title: {
    text: '残差图'
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
    name: ' 时间 ',
    boundaryGap: false,
    data: read("datatime")
  },
  yAxis: {
    type: 'value',
    name:' 残差值 ',
    axisLabel: {
      formatter: '{value} KW'
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
      name: '残差',
      type: 'line',
      data: read("abs"),
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        data: [{ type: 'average', name: 'Avg' }]
      }
    },
  ]
};

option && myChart.setOption(option);
})



onMounted(()=>{
var myChart = echarts.init(chart3.value);
var option = {
    title: {
    text: '双指标散点图',
    // subtext: 'Data from: Heinz 2003'
  },
  grid: {
    left: '3%',
    right: '7%',
    bottom: '7%',
    containLabel: true
  },
  tooltip: {
    // trigger: 'axis',
    showDelay: 0,
    formatter: function (params) {
      if (params.value.length > 1) {
        return (
          params.seriesName +
          ' : ' +
          params.value[1] +
          'KW '
        );
      } else {
        return (
          params.name +
          ' : ' +
          params.value +
          'KW '
        );
      }
    },
    axisPointer: {
      show: true,
      type: 'cross',
      lineStyle: {
        type: 'dashed',
        width: 1
      }
    }
  },
  toolbox: {
    feature: {
      dataZoom: {},
      brush: {
        type: ['rect', 'polygon', 'clear']
      },
      saveAsImage: {}
    }
  },
  brush: {},
  legend: {
    data: ['Original', 'Predicted'],
    left: 'center',
    bottom: 10
  },
  xAxis: [
    {
      type: 'value',
      name: 'Sys Pre',
      scale: true,
      axisLabel: {
        formatter: '{value} KW'
      },
      splitLine: {
        show: false
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: 'Power',
      scale: true,
      axisLabel: {
        formatter: '{value} KW'
      },
      splitLine: {
        show: false
      }
    }
  ],
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
      name: 'Original',
      type: 'scatter',
      emphasis: {
        focus: 'series'
      },
      // prettier-ignore
      data: read("data1"),
      markArea: {
        silent: true,
        itemStyle: {
          color: 'transparent',
          borderWidth: 1,
          borderType: 'dashed'
        },
        data: [
          [
            {
              name: 'Original Data Range',
              xAxis: 'min',
              yAxis: 'min'
            },
            {
              xAxis: 'max',
              yAxis: 'max'
            }
          ]
        ]
      },
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        lineStyle: {
          type: 'solid'
        },
        // data: [{ type: 'average', name: 'AVG' }, { xAxis: 160 }]
      }
    },
    {
      name: 'Predicted',
      type: 'scatter',
      emphasis: {
        focus: 'series'
      },
      // prettier-ignore
      data: read("data2"),
      markArea: {
        silent: true,
        itemStyle: {
          color: 'transparent',
          borderWidth: 1,
          borderType: 'dashed'
        },
        data: [
          [
            {
              name: 'Predicted Data Range',
              xAxis: 'min',
              yAxis: 'min'
            },
            {
              xAxis: 'max',
              yAxis: 'max'
            }
          ]
        ]
      },
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        lineStyle: {
          type: 'solid'
        },
        // data: [{ type: 'average', name: 'Average' }, { xAxis: 170 }]
      }
    }
  ]
}
option && myChart.setOption(option);
})


// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust){
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    // console.log(usn);
    document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
    document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
  }
});

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);

watch(
    layoutConfig.theme,
    () => {
        setColorOptions();
        setChart();
    },
    { immediate: true }
);
// 发送请求到后端进行预测
// 根据风机代号从后端获取时间范围
const LSTMPredict = () => {
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  if (ust){
    axios.post('http://39.104.62.62:5000/predict', {
      usn,
      ust,
      uet
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
        // console.log('test')
        // console.log(ret.data.msg);
      }else { // 成功
        console.log(ret.data);
        var oYD15 = ret.original
        var datatime= ret.data["DATATIME"];
        var pYD15 =ret.data['YD15'];
        var sysYD15=ret.sys_pre
        // console.log(pYD15)
        // console.log(pYD15[1])
        // console.log(typeof pYD15[1])
    //     for (let i = 0; i < pYD15.length; i++) {
    //     pYD15[i]=parseFloat(pYD15[i]);
    // }
        // console.log(pYD15)
        // console.log(typeof pYD15[1])
        // pYD15=parseFloat(pYD15);
        var save = function (name,arr) {
            localStorage.setItem(name,JSON.stringify(arr))
        }
        var read=function(name){
            return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
        }
        save("oYD15",oYD15)
        save("pYD15",pYD15);
        save("datatime",datatime)
        save("sysYD15",sysYD15)
        var subtractedList = [];
        for (var i = 0; i < oYD15.length; i++) {
        var diff = oYD15[i] - pYD15[i];
        subtractedList.push(Math.abs(diff));
        }
        save("abs", subtractedList);
        // const data1 = datatime.map((item, index) => [item, oYD15[index]]);
        // const data2 = datatime.map((item, index) => [item, pYD15[index]]);
        const data1 = sysYD15.map((item, index) => [item, oYD15[index]]);
        const data2 = sysYD15.map((item, index) => [item, pYD15[index]]);
        save("data1",data1);
        save("data2",data2);
        // localStorage.setItem('pYD15', pYD15);
        // let arr = Object.values(localStorage.getItem("pYD15"));
        // console.log(arr);
        // console.log(typeof arr[0]);
        
        // console.log(typeof localStorage.getItem("pYd15"))
        // console.log(localStorage.getItem("pYd15")[1])
        // localStorage.setItem('datatime', datatime);
      }
    }).catch(err => {
      console.log(err);
    });
  }
  
};



// const VITE_API_URL = localStorage.getItem("ust");
// console.log(ust);
// function executeAfterloadedtemplate(){
//
//     console.log(ust);
//     if (ust){
//       let usn = localStorage.getItem("usn");
//       let st = localStorage.getItem("st");
//       let et = localStorage.getItem("et");
//       let ust = localStorage.getItem("ust");
//       let uet = localStorage.getItem("uet");
//       console.log(usn);
//       document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
//       document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
//       document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
//     }
// }
// 渲染完静态页面后执行
// eslint-disable-next-line no-undef
// $(window).load(function(){
//   const ust = localStorage.getItem("ust");
//   console.log(ust);
//   if (ust){
//     let usn = localStorage.getItem("usn");
//     let st = localStorage.getItem("st");
//     let et = localStorage.getItem("et");
//     let ust = localStorage.getItem("ust");
//     let uet = localStorage.getItem("uet");
//     console.log(usn);
//     document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
//     document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
//     document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
//   }
// })
//
// //  等待页面加载完毕后执行
// window.onload = function () {
//   const ust = localStorage.getItem("ust");
//   console.log(ust);
//   if (ust){
//     let usn = localStorage.getItem("usn");
//     let st = localStorage.getItem("st");
//     let et = localStorage.getItem("et");
//     let ust = localStorage.getItem("ust");
//     let uet = localStorage.getItem("uet");
//     console.log(usn);
//     document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
//     document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
//     document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
//   }
// }
// 等该template加载完毕后执行
// window.onload = function () {
//   const ust = localStorage.getItem("ust");
//   console.log(ust);
//   if (ust){
//     let usn = localStorage.getItem("usn");
//     let st = localStorage.getItem("st");
//     let et = localStorage.getItem("et");
//     let ust = localStorage.getItem("ust");
//     let uet = localStorage.getItem("uet");
//     console.log(usn);
//     document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
//     document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
//     document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
//   }
// }

// document.addEventListener('DOMContentLoaded', function() {
//   //js代码
//   const ust = localStorage.getItem("ust");
//   console.log(ust);
//   if (ust){
//     let usn = localStorage.getItem("usn");
//     let st = localStorage.getItem("st");
//     let et = localStorage.getItem("et");
//     let ust = localStorage.getItem("ust");
//     let uet = localStorage.getItem("uet");
//     console.log(usn);
//     document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
//     document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
//     document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
//   }
// });

</script>


<template>
    <div class="grid p-fluid">

        <!-- 文本 -->
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>Model Introduction</h5>
                <Accordion :activeIndex="0">
                    <AccordionTab header="Introduction">
                        <p class="line-height-3 m-0">
                            模型简介
                        </p>
                    </AccordionTab>
                    <!-- <AccordionTab header="Advantages">
                        <p class="line-height-3 m-0">
                            模型优势
                        </p>
                    </AccordionTab> -->
                    <AccordionTab header="Reference">
                        <p class="line-height-3 m-0">
                            参考文献
                        </p>
                    </AccordionTab>
                </Accordion>
            </div>
        </div>

        <div class="col-12 md:col-6">
            <div class="card">
                <h5>LSTM</h5>
                <Panel header="参数确认" :toggleable="true">
                    <p class="line-height-3 m-0" id="Fan">
                        已选择的风机代号为：
                    </p>
                    <p class="line-height-3 m-0" id="TimeRange">
                        对应的时间范围为：
                    </p>
                    <p class="line-height-3 m-0" id="UserTimeRange">
                        用户选择的时间范围为：
                    </p>
                    <p>
                    </p>
                    <Button label="开始预测" class="mr-2 mb-2" @click="LSTMPredict" />
                </Panel>
            </div>
        </div>

        <!-- 列表 -->
        <div class="col-12">
            <div class="card">
                <h5>Parameter details</h5>
                <TreeTable :value="model1Value"  v-model:selectionKeys="selectedTreeTableValue">
                    <!-- <template #header> Parameter details</template> -->
                    <Column field="name" header="Parameter"></Column>
                    <Column field="size" header="Size"></Column>
                    <Column field="type" header="Introduction"></Column>
                </TreeTable>
            </div>
        </div>


        <!-- 滑轮图 -->
        <!-- <div class="col-12">
            <div class="card">
                <h5>Images</h5>
                <Galleria :value="images" :responsiveOptions="galleriaResponsiveOptions" :numVisible="7" :circular="true" containerStyle="max-width: 800px; margin: auto">
                    <template #item="slotProps">
                        <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 80%; display: block" />
                    </template>
                    <template #thumbnail="slotProps">
                        <img :src="slotProps.item.thumbnailImageSrc" :alt="slotProps.item.alt" tyle="width: 100%; display: block;" />
                    </template>
                </Galleria>
            </div>
        </div> -->

        <div class="col-12">
            <div class="card">
                    <div ref="chart1" style="width: 1000px; height: 400px;"></div>
                <!-- <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false" :responsiveOptions="carouselResponsiveOptions">
                    <template #item="product">
                        <div class="product-item">
                                <Center class="mb-3">
                                    <img :src="'demo/images/product/' + product.data.image" :alt="product.data.name" class="product-image" />
                                </Center>
                                <Center class="mt-0 mb-3" position="center">
                                        Comments Here (不能超过一行)
                                </Center>
                                <Center class="car-buttons mt-5">
                                        <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search"></Button>
                                        <Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>
                                        <Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>
                                </Center>
                        </div>
                    </template>
                </Carousel> -->
            </div>
        </div>
        <div class="col-12">
            <div class="card">
                    <div ref="chart2" style="width: 1000px; height: 400px;"></div>
            </div>
        </div>
        <div class="col-12">
            <div class="card">
                    <div ref="chart3" style="width: 1000px; height: 600px;"></div>
            </div>
        </div>

        <!-- <div class="col-12">
            <div class="card">
                <h5>Carousel</h5>
                <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false" :responsiveOptions="carouselResponsiveOptions">
                    <template #item="product">
                        <div class="product-item">
                                <div class="mb-3">
                                    <img :src="'demo/images/product/' + product.data.image" :alt="product.data.name" class="product-image" />
                                </div>
                                <h6 class="mt-0 mb-3"> Comments Here </h6>
                                <div class="car-buttons mt-5">
                                        <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search"></Button>
                                        <Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>
                                        <Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>
                                </div>
                        </div>
                    </template>
                </Carousel>
            </div>
        </div> -->

        <!-- <div class="col-12">
            <div class="card">
                <h5>Image</h5>
                <div class="flex justify-content-center">
                    <Image :src="'demo/images/galleria/galleria11.jpg'" alt="Image" width="250" preview />
                </div>
            </div>
        </div> -->
    </div>
</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
