clc;
clear;

%% constantes de primer dato y tamaño de muestra

folder = uigetdir();
fileList = dir(fullfile(folder, '*.csv'));
fileList = {fileList.name};

media_error_x_tr = [];
media_error_x_uwb = [];
media_error_y_tr = [];
media_error_y_uwb = [];
max_error_x_tr = [];
max_error_x_uwb = [];
max_error_y_tr = [];
max_error_y_uwb = [];
media_error_distancia_tr = [];
media_error_distancia_uwb= [];
RMSE_tr = [];
RMSE_uwb = [];

k = 1;
m = 1;
n = 1;

eje_X = [];
eje_Y = [];


for f = 1:size(fileList,2)

    T = readtable(string(fileList(f)));
    disp(string(fileList(f)))
    
    tamano = size(fileList);
    start_index = 1;
    samples = size(T,1);

    switch f
        case {1,2}
            pto_trabajo_X = 1000;
            pto_trabajo_Y = 1000;
        case {3,4}
            pto_trabajo_X = 1000;
            pto_trabajo_Y = 1500;
        case {5,6}
            pto_trabajo_X = 1000;
            pto_trabajo_Y = 2000;
        case {7,8}
            pto_trabajo_X = 1000;
            pto_trabajo_Y = 2500;
        case {9,10}
            pto_trabajo_X = 1000;
            pto_trabajo_Y = 3000;
        case {11,12}
            pto_trabajo_X = 1500;
            pto_trabajo_Y = 1000;
        case {13,14}
            pto_trabajo_X = 1500;
            pto_trabajo_Y = 1500;
        case {15,16}
            pto_trabajo_X = 1500;
            pto_trabajo_Y = 2000;
        case {17,18}
            pto_trabajo_X = 1500;
            pto_trabajo_Y = 2500;
        case {19,20}
            pto_trabajo_X = 1500;
            pto_trabajo_Y = 3000;
        case {21,22}
            pto_trabajo_X = 2000;
            pto_trabajo_Y = 1000;
        case {23,24}
            pto_trabajo_X = 2000;
            pto_trabajo_Y = 1500;
        case {25,26}
            pto_trabajo_X = 2000;
            pto_trabajo_Y = 2000;
        case {27,28}
            pto_trabajo_X = 2000;
            pto_trabajo_Y = 2500;
        case {29,30}
            pto_trabajo_X = 2000;
            pto_trabajo_Y = 3000;
        case {31,32}
            pto_trabajo_X = 2500;
            pto_trabajo_Y = 1000;
        case {33,34}
            pto_trabajo_X = 2500;
            pto_trabajo_Y = 1500;
        case {35,36}
            pto_trabajo_X = 2500;
            pto_trabajo_Y = 2000;
        case {37,38}
            pto_trabajo_X = 2500;
            pto_trabajo_Y = 2500;
        case {39,40}
            pto_trabajo_X = 2500;
            pto_trabajo_Y = 3000;
        case {41,42}
            pto_trabajo_X = 3000;
            pto_trabajo_Y = 1000;
        case {43,44}
            pto_trabajo_X = 3000;
            pto_trabajo_Y = 1500;
        case {45,46}
            pto_trabajo_X = 3000;
            pto_trabajo_Y = 2000;
        case {47,48}
            pto_trabajo_X = 3000;
            pto_trabajo_Y = 2500;
        case {49,50}
            pto_trabajo_X = 3000;
            pto_trabajo_Y = 3000;
        case {51,52}
            pto_trabajo_X = 3500;
            pto_trabajo_Y = 1000;
        case {53,54}
            pto_trabajo_X = 3500;
            pto_trabajo_Y = 1500;
        case {55,56}
            pto_trabajo_X = 3500;
            pto_trabajo_Y = 2000;
        case {57,58}
            pto_trabajo_X = 3500;
            pto_trabajo_Y = 2500;
        case {59,60}
            pto_trabajo_X = 3500;
            pto_trabajo_Y = 3000;
        case {61,62}
            pto_trabajo_X = 4000;
            pto_trabajo_Y = 1000;
        case {63,64}
            pto_trabajo_X = 4000;
            pto_trabajo_Y = 1500;
        case {65,66}
            pto_trabajo_X = 4000;
            pto_trabajo_Y = 2000;
        case {67,68}
            pto_trabajo_X = 4000;
            pto_trabajo_Y = 2500;
        case {69,70}
            pto_trabajo_X = 4000;
            pto_trabajo_Y = 3000;
    end
    
    if(mod(f,2) ~= 0)
        eje_X(n) = pto_trabajo_X;
        eje_Y(n) = pto_trabajo_Y;
        n = n+1;
    end

    pozyx_data = readtable(string(fileList(f)));
    
    pozyx.time=pozyx_data.rosbagTimestamp;
    pozyx.position.x= pozyx_data.x/1000;
    pozyx.position.y= pozyx_data.y/1000;
    pozyx.position.z= pozyx_data.z/1000;
    
    pozyx_time = pozyx.time/(1e9);
    pozyx_time = pozyx_time-pozyx_time(1);
    pozyx_time = round(pozyx_time,1);
    
    j = 1;
    pozyx_final = [];
    ref = [];
    for i = 0:0.1:pozyx_time(end)
        i = round(i,1);%Incluyo esto para que cuadre el formato de i con pozyx_time
        pozyx_index_time = find(pozyx_time == i);
        if(size(pozyx_index_time,1) ~= 0)
            pozyx_index = pozyx_index_time(end);
            pozyx_final(j,1) = pozyx.position.x(pozyx_index);
            pozyx_final(j,2) = pozyx.position.y(pozyx_index);
            pozyx_final(j,3) = pozyx_time(pozyx_index);
            j = j+1;
        end
    end
    
    %Error del sistema en X e Y
    ref = ones(size(pozyx_final,1),2);
    ref(:,1) = ref(:,1)*(pto_trabajo_X/1000);
    ref(:,2) = ref(:,2)*(pto_trabajo_Y/1000);
    error_pozyx = ref - pozyx_final(:,1:2);
    
    %Distancias euclideas entre puntos
    for i=1:size(error_pozyx,1)
        p1=[pozyx_final(i,1) pozyx_final(i,2)];
        p2 = [ref(i,1) ref(i,2)];
        norm_pozyx(i) = norm(p1-p2);
    end
    norm_pozyx = transpose(norm_pozyx);
    

    
%     %Gráfico de la medida Pozyx
%     figure
%     plot(pozyx_final(:,1),pozyx_final(:,2),'o','color',[0.3010 0.7450 0.9330],'MarkerFaceColor',[0 0 1],'MarkerSize',4);
%     hold on;
%     plot(ref(:,1),ref(:,2),'o','color',[0.8500 0.3250 0.0980],'MarkerFaceColor',[0.8500 0.3250 0.0980],'MarkerSize',10);
%     grid on;
%     xlim([0 pto_trabajo_X/1000]);
%     ylim([0 pto_trabajo_Y/1000]);
%     title('Gráfico de la medida Pozyx: ', fileList(f));
%     xlabel('Posición en x (m)'); 
%     ylabel('Posición en y (m)');
%     legend('Evolución de las medidas', 'Punto de trabajo');
%     
%     %Gráfico del error
%     figure
%     plot(error_pozyx(:,1), 'o', 'color', [0.3010 0.7450 0.9330], 'MarkerFaceColor',[0 0 1]);
%     hold on;
%     plot(error_pozyx(:,2), 'o', 'color','g', 'MarkerFaceColor',[0.4660 0.6740 0.1880]);
%     grid on;
%     title('Error a lo largo de los ejes de coordenadas: ', fileList(f));
%     xlabel('Número de muestra');
%     ylabel('Error (m)');
%     legend('Error en eje X','Error en eje Y')
% 
%     %Gráfico de la norma
%     figure
%     plot(norm_pozyx, 'o', 'color', [0.3010 0.7450 0.9330], 'MarkerFaceColor',[0 0 1]);
%     hold on;
%     grid on;
%     title('Norma: ', fileList(f));
%     xlabel('Número de muestra');
%     ylabel('Norma (m)');
%  
    %Muestra de errores
    %disp('Media del error en x:')
    %disp(mean(abs(error_pozyx(:,1))))
    
    if(mod(f,2) == 0)
        media_error_x_tr(k) = mean(abs(error_pozyx(150:end,1)));
        max_error_x_tr(k) = max(abs(error_pozyx(150:end,1)));
        media_error_y_tr(k) = mean(abs(error_pozyx(150:end,2)));
        max_error_y_tr(k) = max(abs(error_pozyx(150:end,2)));
        media_error_distancia_tr(k) = mean(norm_pozyx(150:end));
        RMSE_tr(k) = sqrt(mean(norm_pozyx(150:end).^2));
        k=k+1;
    else
        media_error_x_uwb(m) = mean(abs(error_pozyx(20:end,1)));
        max_error_x_uwb(m) = max(abs(error_pozyx(20:end,1)));
        media_error_y_uwb(m) = mean(abs(error_pozyx(20:end,2)));
        max_error_y_uwb(m) = max(abs(error_pozyx(20:end,2)));
        media_error_distancia_uwb(m) = mean(norm_pozyx(20:end));
        RMSE_uwb(m) = sqrt(mean(norm_pozyx(20:end).^2));
        m=m+1;
    end

    %disp('Media del error en x:')
    %disp(mean(abs(error_pozyx(:,1))))

    %disp('Error maximo en x:')
    %disp(max(abs(error_pozyx(:,1))))

    
    %disp('Media del error en y:')
    %disp(mean(abs(error_pozyx(:,2))))

    
    %disp('Error maximo en y:')
    %disp(max(abs(error_pozyx(:,2))))

    
    %disp('Media del error en distancia:')
    %disp(mean(norm_pozyx))
    
    %Error RMS
    %disp('Mean square error')
    %disp(mean(norm_pozyx.^2));
    
    %RMSE = sqrt(mean(norm_pozyx.^2));  % Root Mean Squared Error
    %disp('Error RMS')
    %disp(RMSE)
    
    %disp('P90 del error')
    %p90 = prctile(norm_pozyx,50);
    %disp(p90)
    
    %disp('P95 del error')
    %p95 = prctile(norm_pozyx,95);
    %disp(p95)
end

%Gráfico media del error en x tracking
figure
plot3(eje_X, eje_Y, media_error_x_tr, 'o', 'color', 'g', 'MarkerFaceColor','g');
hold on
plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
plot([0 5000 5000 0], [0 4000 0 4000], 'o','color','k','MarkerFaceColor','k','MarkerSize',10)
legend('Media del error en X', 'Marcadores de medidas', 'Marcadores de anchors');
grid on;
title('Media del error en X con algoritmo con filtro');
xlabel('X');
ylabel('Y');
zlabel('Error_X');

% % 
% %Gráfico media del error en x UWB
% figure
% plot3(eje_X, eje_Y, media_error_x_uwb, 'o', 'color', 'g', 'MarkerFaceColor','g');
% hold on
% plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
% plot([0 5000 5000 0], [0 4000 0 4000], 'o','color','k','MarkerFaceColor','k','MarkerSize',10)
% legend('Media del error en X', 'Marcadores de medidas', 'Marcadores de anchors');
% grid on;
% title('Media del error en X con algoritmo sin filtro');
% xlabel('X');
% ylabel('Y');
% zlabel('Error_X');
% 
%Gráfico media del error en Y tracking
figure
plot3(eje_X, eje_Y, media_error_y_tr, 'o', 'color', 'g', 'MarkerFaceColor','g');
hold on
plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
grid on;
title('Media del error en Y con algoritmo con filtro');
xlabel('X');
ylabel('Y');
zlabel('Error_Y');
% 
% %Gráfico media del error en Y UWB
% figure
% plot3(eje_X, eje_Y, media_error_y_uwb, 'o', 'color', 'g', 'MarkerFaceColor','g');
% hold on
% plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
% grid on;
% title('Media del error en Y en UWB');
% xlabel('X');
% ylabel('Y');
% zlabel('Error_Y');

%Gráfico media error distancia tracking
figure
plot3(eje_X, eje_Y, media_error_distancia_tr, 'o', 'color', 'g', 'MarkerFaceColor','g');
hold on
plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
grid on;
title('Media del error distancia con algoritmo con filtro');
xlabel('X');
ylabel('Y');
zlabel('Error');
% 
% %Gráfico media error distancia uwb
% figure
% plot3(eje_X, eje_Y, media_error_distancia_uwb, 'o', 'color', 'g', 'MarkerFaceColor','g');
% hold on
% plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
% grid on;
% title('Media del error distancia con UWB');
% xlabel('X');
% ylabel('Y');
% zlabel('Error');

%Gráfico RMSE tracking
figure
plot3(eje_X, eje_Y, RMSE_tr, 'o', 'color', 'g', 'MarkerFaceColor','g');
hold on
plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
grid on;
% [X,Y] = meshgrid(1000:500:4000, 1000:500:3000);
% N = meshgrid(norm_pozyx);
% Z(:,1) = RMSE_tr(1:5);
% Z(:,2) = RMSE_tr(6:11);
% Z(:,3) = RMSE_tr(12:17);
% Z(:,4) = RMSE_tr(18:23);
% Z(:,5) = RMSE_tr(24:29);
% Z(:,6) = RMSE_tr(30:35);
% 
% mesh(X,Y,Z);
title('RMSE con algoritmo con filtro');
xlabel('X');
ylabel('Y');
zlabel('RMSE');

% %Gráfico RMSE UWB
% figure
% plot3(eje_X, eje_Y, RMSE_uwb, 'o', 'color', 'g', 'MarkerFaceColor','g');
% hold on
% plot(eje_X, eje_Y, 'o','color',[0 0.4470 0.7410],'MarkerFaceColor',[0.3010 0.7450 0.9330],'MarkerSize',10)
% grid on;
% title('RMSE con UWB');
% xlabel('X');
% ylabel('Y');
% zlabel('RMSE');