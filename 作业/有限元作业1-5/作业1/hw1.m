%% =========================================================
%  有限元求解  -u'' = f,  0<x<1,  u(0)=u(1)=0
%  u(x) = (x-1)*sin(x),  f(x) = -(2cos(x) - (x-1)*sin(x))
%% =========================================================
clear; clc;

Nlist = [10 20 40 80];
nN    = length(Nlist);
errL2 = zeros(1,nN);   errH1 = zeros(1,nN);

for k = 1:nN
    N  = Nlist(k);
    h  = 1/(N+1);
    x  = (0:(N+1))'*h;          % 全部 N+2 个节点(列向量), x(1)=0, x(end)=1
    xi = x(2:N+1);              % 内节点 x_1,...,x_N

    % ---------- 刚度矩阵 A ----------
    A = (2/h)*eye(N) - (1/h)*(diag(ones(N-1,1),1) + diag(ones(N-1,1),-1));

    % ---------- 载荷向量 b (含边界节点贡献) ----------
    M  = (h/6)*(4*eye(N) + diag(ones(N-1,1),1) + diag(ones(N-1,1),-1));
    b  = M*ffun(xi);
    b(1) = b(1) + (h/6)*ffun(x(1));     % 补 (h/6)*f(x_0)
    b(N) = b(N) + (h/6)*ffun(x(end));   % 补 (h/6)*f(x_{N+1})

    U = A \ b;

    errL2(k) = computeError(U, x, h, 0);
    errH1(k) = computeError(U, x, h, 1);
end

% ---------- 收敛阶 (注意: 必须用点除 ./) ----------
ordL2 = log(errL2(1:nN-1)./errL2(2:nN)) ./ log(Nlist(2:nN)./Nlist(1:nN-1));
ordH1 = log(errH1(1:nN-1)./errH1(2:nN)) ./ log(Nlist(2:nN)./Nlist(1:nN-1));

% ---------- 输出表格 ----------
fprintf('   N      L2 error      order     H1 error      order\n');
fprintf('---------------------------------------------------------\n');
for k = 1:nN
    if k == 1
        fprintf('%4d   %.4e       --     %.4e       --\n', Nlist(k), errL2(k), errH1(k));
    else
        fprintf('%4d   %.4e   %6.3f   %.4e   %6.3f\n', ...
                Nlist(k), errL2(k), ordL2(k-1), errH1(k), ordH1(k-1));
    end
end

% ==================== 子函数 ====================
function y = ffun(x)
    y = -(2*cos(x) - (x-1).*sin(x));
end

function y = uexact(x)
    y = (x-1).*sin(x);
end

function y = duexact(x)
    y = sin(x) + (x-1).*cos(x);
end

function err = computeError(U, x, h, iflag)
% iflag = 0: ||u - u_h||_{L2};   iflag = 1: ||u - u_h||_{H1}
    N  = length(U);
    Uf = [0; U; 0];             % 补上边界值 u(0)=u(1)=0
    m  = 20;                    % 每个单元细分 m 段
    dx = h/m;                   % 细分步长(等距)
    e2 = 0;
    for j = 1:N+1               % 第 j 个单元 I_j = [x(j), x(j+1)]
        xs = x(j) + dx*(0:m);   % 单元内的求积节点(行向量, 不用 linspace)
        uh = Uf(j)*(x(j+1)-xs)/h + Uf(j+1)*(xs-x(j))/h;   % u_h 线性插值
        ue = uexact(xs);
        if iflag == 0
            g = (ue - uh).^2;
        else
            duh = (Uf(j+1)-Uf(j))/h;    % u_h' 在单元上为常数
            g   = (ue-uh).^2 + (duexact(xs)-duh).^2;
        end
        % 复合梯形公式(手工实现, 避开 trapz 的兼容性问题):
        e2 = e2 + dx*( sum(g) - 0.5*(g(1) + g(m+1)) );
    end
    err = sqrt(e2);
end
