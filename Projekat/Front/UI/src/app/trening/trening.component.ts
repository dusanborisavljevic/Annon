import { Component, OnInit } from '@angular/core';
import { ChartModel } from 'ag-grid-community';
import{webSocket} from 'rxjs/webSocket'
import { SignalRService } from '../shared/signal-r.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-trening',
  templateUrl: './trening.component.html',
  styleUrls: ['./trening.component.css']
})
export class TreningComponent implements OnInit {
  ind=false;
  
  constructor(private signalR:SignalRService) { 
    
  }

  

  ngOnInit(): void {
    this.signalR.startConnection();
    this.signalR.addTransferChartDatalistener();
    this.signalR.sendRequest();
    
  }
  SendtoBack()
  {
    const myChart = new Chart('myChart', {
      type: 'line',
      data: {
          labels: ['Epoch','Loss'],
          datasets: [{
              label: 'Epoch',
              data: [this.signalR.data[0]['epocheNumber'][0],this.signalR.data[1]['epocheNumber'][0],this.signalR.data[2]['epocheNumber'][0],this.signalR.data[3]['epocheNumber'][0]],
              backgroundColor: "black",
              borderColor: "black",
              borderWidth: 1
          },
          {
            label: 'Loss',
              data: [5,8,3,4],
              backgroundColor: "red",
              borderColor: "red",
              borderWidth: 1
          }
        
        ]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
   this.ind=true;
   
  }

}






