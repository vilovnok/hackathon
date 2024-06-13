import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
@Injectable({
  providedIn: 'root'
})
export class DataService {
  private address= environment.API_BASE_URL;

  constructor(private http:HttpClient) { }

  handle_post_requests(userObject: any, endpoint: string) {    
    return this.http.post<any>(`${this.address}/${endpoint}`, userObject)
  }

  handle_get_all_requests(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.address}/${endpoint}`)
  }
}
