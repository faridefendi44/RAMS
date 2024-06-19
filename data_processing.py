import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from plot import plot_interactive_weibull

# def process_failure_rate(data):
#     if 'LRU (L3)' in data.columns:
#         lru_values = data['LRU (L3)'].unique().tolist()
#         lru_values.insert(0, '')
#         selected_lru = st.sidebar.selectbox('Pilih Nilai LRU (L3)', options=lru_values, index=0)
#         if selected_lru:
#             filtered_data = data.loc[data['LRU (L3)'] == selected_lru, ['TTF (jam)', 'Total Jumlah Gangguan']]
#             filtered_data['Failure Rate'] = filtered_data['Total Jumlah Gangguan'] / filtered_data['TTF (jam)']
#             st.write(filtered_data.style.format({'Failure Rate': '{:.9f}'}))

#             average_failure_rate = filtered_data['Failure Rate'].mean()
#             st.write(f"Rata-rata Failure Rate: {average_failure_rate:.9f}")
#             plot_interactive_weibull(filtered_data['TTF (jam)'])
#         else:
#             data['Failure Rate'] = data['Total Jumlah Gangguan'] / data['TTF (jam)']
#             st.write(data[['TTF (jam)', 'Total Jumlah Gangguan', 'Failure Rate']].style.format({'Failure Rate': '{:.9f}'}))

#             average_failure_rate = data['Failure Rate'].mean()
#             st.write(f"Rata-rata Failure Rate: {average_failure_rate:.9f}")
#             plot_interactive_weibull(data['TTF (jam)'])
#     else:
#         st.sidebar.warning('Kolom "LRU (L3)" tidak ditemukan dalam data.')

def process_failure_rate(data):
    if 'Klasifikasi Komponen (L1)' in data.columns and 'Klasifikasi System/ Subsystem (L2)' in data.columns and 'LRU (L3)' in data.columns:
        l1_values = data['Klasifikasi Komponen (L1)'].unique().tolist()
        l1_values.insert(0, '')
        selected_l1 = st.sidebar.selectbox('Pilih Klasifikasi Komponen (L1)', options=l1_values, index=0)

        if selected_l1:
            l2_values = data.loc[data['Klasifikasi Komponen (L1)'] == selected_l1, 'Klasifikasi System/ Subsystem (L2)'].unique().tolist()
            l2_values.insert(0, '')
            selected_l2 = st.sidebar.selectbox('Pilih Klasifikasi System/ Subsystem (L2)', options=l2_values, index=0)
        else:
            selected_l2 = ''

        if selected_l1 and selected_l2:
            l3_values = data.loc[(data['Klasifikasi Komponen (L1)'] == selected_l1) & (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2), 'LRU (L3)'].unique().tolist()
            l3_values.insert(0, '')
            selected_l3 = st.sidebar.selectbox('Pilih LRU (L3)', options=l3_values, index=0)
        else:
            selected_l3 = ''

        if selected_l1 and selected_l2 and selected_l3:
            filtered_data = data[(data['Klasifikasi Komponen (L1)'] == selected_l1) & 
                                 (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2) &
                                 (data['LRU (L3)'] == selected_l3)].copy()
        elif selected_l1 and selected_l2:
            filtered_data = data[(data['Klasifikasi Komponen (L1)'] == selected_l1) & 
                                 (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2)].copy()
        elif selected_l1:
            filtered_data = data[data['Klasifikasi Komponen (L1)'] == selected_l1].copy()
        else:
            filtered_data = data.copy()

        filtered_data['Failure Rate'] = filtered_data['Total Jumlah Gangguan'] / filtered_data['TTF (jam)']
        st.write(filtered_data[['TTF (jam)', 'Total Jumlah Gangguan', 'Failure Rate']].style.format({'Failure Rate': '{:.9f}'}))

        # st.write(filtered_data.style.format({'Failure Rate': '{:.9f}'}))

        average_failure_rate = filtered_data['Failure Rate'].mean()
        st.write(f"Rata-rata Failure Rate: {average_failure_rate:.9f}")
        plot_interactive_weibull(filtered_data['TTF (jam)'])
    else:
        st.sidebar.warning('Kolom "Klasifikasi Komponen (L1)", "Klasifikasi System/ Subsystem (L2)", atau "LRU (L3)" tidak ditemukan dalam data.')

def process_availability(data):
        if 'Klasifikasi Komponen (L1)' in data.columns and 'Klasifikasi System/ Subsystem (L2)' in data.columns:
            l1_values = data['Klasifikasi Komponen (L1)'].unique().tolist()
            l1_values.insert(0, '')
            selected_l1 = st.sidebar.selectbox('Pilih Klasifikasi Komponen (L1)', options=l1_values, index=0)
            if selected_l1:
                l2_values = data.loc[data['Klasifikasi Komponen (L1)'] == selected_l1, 'Klasifikasi System/ Subsystem (L2)'].unique().tolist()
                l2_values.insert(0, '')  
                selected_l2 = st.sidebar.selectbox('Pilih Klasifikasi System/ Subsystem (L2)', options=l2_values, index=0)
            else:
                selected_l2 = ''
            if selected_l1 and selected_l2:
                l3_values = data.loc[(data['Klasifikasi Komponen (L1)'] == selected_l1) & (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2), 'LRU (L3)'].unique().tolist()
                l3_values.insert(0, '') 
                selected_l3 = st.sidebar.selectbox('Pilih LRU (L3)', options=l3_values, index=0)
            else:
                selected_l3 = ''
            if selected_l1 and selected_l2 and selected_l3:
                filtered_data = data[(data['Klasifikasi Komponen (L1)'] == selected_l1) & 
                                    (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2) &
                                    (data['LRU (L3)'] == selected_l3)].copy()
                filtered_data['MTBF'] = np.where((filtered_data['Jenis service'] == 'Perbaikan') | 
                                 (filtered_data['Jenis service'] == 'Perawatan') | 
                                 (filtered_data['Jenis service'] == 'Intermittent'), 
                                 filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                 0)
                filtered_data['MTTF'] = np.where((filtered_data['Jenis service'] == 'Penggantian Komponen') |  
                                                (filtered_data['Jenis service'] == 'Pertukaran Komponen'), 
                                                filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                                0)                       
                filtered_data['tgl & waktu selelsai tdl'] = pd.to_datetime(filtered_data['tgl & waktu selelsai tdl'], format='%d/%m/%Y %H:%M')
                filtered_data['Tgl & waktu'] = pd.to_datetime(filtered_data['Tgl & waktu'], format='%d/%m/%Y %H:%M')
                filtered_data['MTTR'] = (((filtered_data['tgl & waktu selelsai tdl']) - (filtered_data['Tgl & waktu'])).dt.total_seconds() / 3600) * (20/24)
                filtered_data['Availability'] = np.where((filtered_data['MTTR'] >= 0), 
                                                        np.where((filtered_data['MTBF'] > 0), (filtered_data['MTBF'] / (filtered_data['MTBF'] + filtered_data['MTTR'])) * 100, (filtered_data['MTTF'] / (filtered_data['MTTF'] + filtered_data['MTTR'])) * 100 ),
                                                        0)
                filtered_data['Availability'] = filtered_data['Availability'].round(2)
                filtered_data['Availability'] = filtered_data['Availability'].astype(str) + '%'
                st.write('Data Keseluruhan L3')
                st.write(filtered_data[['TTF (jam)','LRU (L3)', 'Total Jumlah Gangguan', 'MTBF', 'MTTF', 'MTTR' , 'Availability']])
                st.write('Data Rata Rata')
                if not filtered_data.empty:
                    filtered_data_with_mttf = filtered_data[filtered_data['MTTF'] > 0]
                    filtered_data_with_mtbf = filtered_data[filtered_data['MTBF'] > 0]
                    if not filtered_data_with_mttf.empty:
                        def calculate_avg_mttf(group):
                            mttf_sum = group['MTTF'].mean()
                            return mttf_sum
                        avg_mttf_per_l3 = filtered_data_with_mttf.groupby('LRU (L3)').apply(calculate_avg_mttf).reset_index(name='avg_mttf')
                    if not filtered_data_with_mtbf.empty:
                        def calculate_avg_mtbf(group):
                            mtbf_sum = group['MTBF'].mean()
                            return mtbf_sum 
                        avg_mtbf_per_l3 = filtered_data_with_mtbf.groupby('LRU (L3)').apply(calculate_avg_mtbf).reset_index(name='avg_mtbf')
                    if not filtered_data_with_mttf.empty and not filtered_data_with_mtbf.empty:
                        combined_avg = pd.merge(avg_mttf_per_l3, avg_mtbf_per_l3, on='LRU (L3)', how='outer')
                        st.write(combined_avg)
                    elif not filtered_data_with_mttf.empty:
                        st.write(avg_mttf_per_l3)
                    elif not filtered_data_with_mtbf.empty:
                        st.write(avg_mtbf_per_l3)
                    else:
                        st.warning("Tidak ada data dengan MTTF atau MTBF yang lebih besar dari 0 yang memenuhi kriteria untuk ditampilkan.")
                else:
                    st.warning("Tidak ada data yang memenuhi kriteria untuk ditampilkan.")
                    
                    
            elif selected_l1 and selected_l2 :
                filtered_data = data[(data['Klasifikasi Komponen (L1)'] == selected_l1) & 
                                    (data['Klasifikasi System/ Subsystem (L2)'] == selected_l2)].copy()
                filtered_data['MTBF'] = np.where((filtered_data['Jenis service'] == 'Perbaikan') | 
                                 (filtered_data['Jenis service'] == 'Perawatan') | 
                                 (filtered_data['Jenis service'] == 'Intermittent'), 
                                 filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                 0)
                filtered_data['MTTF'] = np.where((filtered_data['Jenis service'] == 'Penggantian Komponen') |  
                                                (filtered_data['Jenis service'] == 'Pertukaran Komponen'), 
                                                filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                                0)
                filtered_data['tgl & waktu selelsai tdl'] = pd.to_datetime(filtered_data['tgl & waktu selelsai tdl'], format='%d/%m/%Y %H:%M')
                filtered_data['Tgl & waktu'] = pd.to_datetime(filtered_data['Tgl & waktu'], format='%d/%m/%Y %H:%M')
                filtered_data['MTTR'] = (((filtered_data['tgl & waktu selelsai tdl']) - (filtered_data['Tgl & waktu'])).dt.total_seconds() / 3600) * (20/24)
                filtered_data_with_mtbf = filtered_data[filtered_data['MTBF'] > 0]
                filtered_data_with_mttf = filtered_data[filtered_data['MTTF'] > 0]
                filtered_data_with_mttr = filtered_data[filtered_data['MTTR'] > 0]
                avg_mtbf_per_l3 = filtered_data_with_mtbf.groupby('LRU (L3)').agg(avg_mtbf=('MTBF', 'mean')).reset_index()                
                avg_mttr_per_l3 = filtered_data_with_mttr.groupby('LRU (L3)').agg(avg_mttr=('MTTR', 'mean')).reset_index()
                avg_mttf_per_l3 = filtered_data_with_mttf.groupby('LRU (L3)').agg(avg_mttf=('MTTF', 'mean')).reset_index()
                avg_mtbf_mttf_per_l3 = avg_mtbf_per_l3.merge(avg_mttr_per_l3, on='LRU (L3)', how='outer').merge(avg_mttf_per_l3, on='LRU (L3)', how='outer')
                if not avg_mtbf_mttf_per_l3.empty:
                    overall_avg_mttf = avg_mtbf_mttf_per_l3['avg_mttf'].mean()
                else:
                    overall_avg_mttf = None
                if not avg_mtbf_mttf_per_l3.empty:
                    overall_avg_mtbf = avg_mtbf_mttf_per_l3['avg_mtbf'].mean()
                else:
                    overall_avg_mtbf = None
                filtered_data['tgl & waktu selelsai tdl'] = pd.to_datetime(filtered_data['tgl & waktu selelsai tdl'], format='%d/%m/%Y %H:%M')
                filtered_data['Tgl & waktu'] = pd.to_datetime(filtered_data['Tgl & waktu'], format='%d/%m/%Y %H:%M')
                filtered_data['MTTR'] = (((filtered_data['tgl & waktu selelsai tdl']) - (filtered_data['Tgl & waktu'])).dt.total_seconds() / 3600) * (20/24)
                filtered_data['Availability'] = np.where((filtered_data['MTTR'] >= 0), 
                                                        np.where((filtered_data['MTBF'] > 0), (filtered_data['MTBF'] / (filtered_data['MTBF'] + filtered_data['MTTR'])) * 100, (filtered_data['MTTF'] / (filtered_data['MTTF'] + filtered_data['MTTR'])) * 100 ),
                                                        0)
                filtered_data['Availability'] = filtered_data['Availability'].round(2)
                filtered_data['Availability'] = filtered_data['Availability']
                filtered_data = filtered_data[filtered_data['Availability'] != 0]
                if not filtered_data.empty:
                    avg_availability_per_l3 = {}
                    for l3_category, group_data in filtered_data.groupby('LRU (L3)'):
                        group_data_filtered = group_data[group_data['Availability'] > 0]  
                        if not group_data_filtered.empty:
                            avg_availability = group_data_filtered['Availability'].mean()
                            avg_availability_per_l3[l3_category] = avg_availability
                    avg_availability_df = pd.DataFrame(list(avg_availability_per_l3.items()), columns=['LRU (L3)', 'Avg Availability'])
                    total_avg_availability = avg_availability_df['Avg Availability'].mean()
                    final_df = avg_mtbf_mttf_per_l3.merge(avg_availability_df, on='LRU (L3)', how='outer')
                    st.write(final_df)
                else:
                    st.warning("Tidak ada data yang memenuhi kriteria untuk ditampilkan.")
                st.write("Nilai MTTF L2", selected_l2, 'adalah:',overall_avg_mttf)
                st.write("Nilai MTBF L2", selected_l2, 'adalah:',overall_avg_mtbf)
                st.write(f"Nilai Availability L2 {selected_l2}: {total_avg_availability:.2f}%")
                if not filtered_data.empty:
                    avg_availability = filtered_data.groupby('LRU (L3)')['Availability'].mean().reset_index()
                    fig = go.Figure(data=[go.Bar(x=avg_availability['LRU (L3)'], y=avg_availability['Availability'])])
                    fig.update_layout(title='Average Availability by LRU (L3)',
                                    xaxis_title='LRU (L3)',
                                    yaxis_title='Average Availability',
                                    yaxis=dict(range=[0, 100]))  
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Tidak ada data yang memenuhi kriteria untuk ditampilkan.")
            elif selected_l1:
                filtered_data = data.loc[data['Klasifikasi Komponen (L1)'] == selected_l1]
                filtered_data['MTBF'] = np.where((filtered_data['Jenis service'] == 'Perbaikan') | 
                                 (filtered_data['Jenis service'] == 'Perawatan') | 
                                 (filtered_data['Jenis service'] == 'Intermittent'), 
                                 filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                 0)
                filtered_data['MTTF'] = np.where((filtered_data['Jenis service'] == 'Penggantian Komponen') |  
                                                (filtered_data['Jenis service'] == 'Pertukaran Komponen'), 
                                                filtered_data['TTF (jam)'] / filtered_data['Total Jumlah Gangguan'], 
                                                0)
                filtered_data['tgl & waktu selelsai tdl'] = pd.to_datetime(filtered_data['tgl & waktu selelsai tdl'], format='%d/%m/%Y %H:%M')
                filtered_data['Tgl & waktu'] = pd.to_datetime(filtered_data['Tgl & waktu'], format='%d/%m/%Y %H:%M')
                filtered_data['MTTR'] = (((filtered_data['tgl & waktu selelsai tdl']) - (filtered_data['Tgl & waktu'])).dt.total_seconds() / 3600) * (20/24)
                filtered_data['Availability'] = np.where((filtered_data['MTTR'] > 0), 
                np.where((filtered_data['MTBF'] > 0), (filtered_data['MTBF'] / (filtered_data['MTBF'] + filtered_data['MTTR'])) * 100, (filtered_data['MTTF'] / (filtered_data['MTTF'] + filtered_data['MTTR'])) * 100 ),
                0)
                filtered_data['Availability'] = filtered_data['Availability'].round(2)
                filtered_data['Availability'] = filtered_data['Availability'].astype(str) + '%'
                st.write(filtered_data[['TTF (jam)', 'LRU (L3)', 'MTBF', 'MTTF', 'MTTR' , 'Availability']])  
            else:
                data['MTBF'] = np.where((data['Jenis service'] == 'Perbaikan') | (data['Jenis service'] == 'Perawatan'), 
                                         data['TTF (jam)'] / data['Total Jumlah Gangguan'], 0)
                data['MTTF'] = np.where((data['Jenis service'] == 'Penggantian Komponen') | (data['Jenis service'] == 'Pertukaran Komponen'), 
                                         data['TTF (jam)'] / data['Total Jumlah Gangguan'], 0)
                filtered_data['tgl & waktu selelsai tdl'] = pd.to_datetime(filtered_data['tgl & waktu selelsai tdl'], format='%d/%m/%Y %H:%M')
                filtered_data['Tgl & waktu'] = pd.to_datetime(filtered_data['Tgl & waktu'], format='%d/%m/%Y %H:%M')
                filtered_data['MTTR'] = (((filtered_data['tgl & waktu selelsai tdl']) - (filtered_data['Tgl & waktu'])).dt.total_seconds() / 3600) * (20/24)
                data['MTTR'] = data['MTTR'].fillna(0)
                data['Availability'] = np.where((data['MTTR'] > 0), 
                np.where((data['MTBF'] > 0), (data['MTBF'] / (data['MTBF'] + data['MTTR'])) * 100, (data['MTTF'] / (data['MTTF'] + data['MTTR'])) * 100 ),
                0)
                data['Availability'] = data['Availability'].round(2)
                data['Availability'] = data['Availability'].astype(str) + '%'
                st.write(data[['TTF (jam)', 'LRU (L3)', 'MTBF', 'MTTF', 'MTTR', 'Availability']])
        else:
            st.sidebar.warning('Kolom "Klasifikasi Komponen (L1)" atau "Klasifikasi System/ Subsystem (L2)" tidak ditemukan dalam data.')