--1.tạo database
CREATE DATABASE QuanLySinhVien;
GO

-- 2. TẠO CÁC BẢNG 

-- [Bảng 1] KHOA
CREATE TABLE KHOA (
    MaKhoa VARCHAR(20) PRIMARY KEY,
    TenKhoa NVARCHAR(100) NOT NULL
);

-- [Bảng 2] GIANGVIEN
CREATE TABLE GIANGVIEN (
    MaGV VARCHAR(20) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    GioiTinh NVARCHAR(10) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    DiaChi NVARCHAR(200),
    Email VARCHAR(100),
    MaKhoa VARCHAR(20) NOT NULL,
    FOREIGN KEY (MaKhoa) REFERENCES KHOA(MaKhoa)
);

-- [Bảng 3] LOPHOC
CREATE TABLE LOPHOC (
    MaLop VARCHAR(20) PRIMARY KEY,
    TenLop NVARCHAR(100) NOT NULL,
    ChuyenNganh NVARCHAR(100),
    CoVanHocTap VARCHAR(20),
    MaKhoa VARCHAR(20),
    FOREIGN KEY (CoVanHocTap) REFERENCES GIANGVIEN(MaGV) ON DELETE SET NULL,
    FOREIGN KEY (MaKhoa) REFERENCES KHOA(MaKhoa)
);

-- [Bảng 4] SINHVIEN
CREATE TABLE SINHVIEN (
    MaSV VARCHAR(20) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    GioiTinh NVARCHAR(10) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    NgaySinh DATE,
    MaLop VARCHAR(20),
    SDT VARCHAR(15),
    DiaChi NVARCHAR(200),
    NamThu INT CHECK (NamThu BETWEEN 1 AND 6),
    KhoaHoc NVARCHAR(20),
    FOREIGN KEY (MaLop) REFERENCES LOPHOC(MaLop)
);

-- [Bảng 5] HOCPHAN
CREATE TABLE HOCPHAN (
    MaHP VARCHAR(20) PRIMARY KEY,
    TenHP NVARCHAR(100) NOT NULL,
    TinChi INT CHECK (TinChi > 0),
    MaKhoa VARCHAR(20),
    FOREIGN KEY (MaKhoa) REFERENCES KHOA(MaKhoa)
);

-- [Bảng 6] DANGKY
CREATE TABLE DANGKY (
    MaSV VARCHAR(20),
    MaHP VARCHAR(20),
    HocKy INT,
    NamHoc NVARCHAR(20),
    PRIMARY KEY (MaSV, MaHP, HocKy, NamHoc),
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV) ON DELETE CASCADE,
    FOREIGN KEY (MaHP) REFERENCES HOCPHAN(MaHP)
);

-- [Bảng 7] DIEM
CREATE TABLE DIEM (
    MaSV VARCHAR(20),
    MaHP VARCHAR(20),
    HocKy INT,
    NamHoc NVARCHAR(20),
    DiemChuyenCan DECIMAL(4,2) CHECK (DiemChuyenCan BETWEEN 0 AND 10),
    DiemBaiTap DECIMAL(4,2) CHECK (DiemBaiTap BETWEEN 0 AND 10),
    DiemGiuaKy DECIMAL(4,2) CHECK (DiemGiuaKy BETWEEN 0 AND 10),
    DiemCuoiKy DECIMAL(4,2) CHECK (DiemCuoiKy BETWEEN 0 AND 10),
    DiemTongKet AS (
        CAST(DiemChuyenCan * 0.1 + DiemBaiTap * 0.2 + DiemGiuaKy * 0.3 + DiemCuoiKy * 0.4 AS DECIMAL(4,2))
    ),
    PRIMARY KEY (MaSV, MaHP, HocKy, NamHoc),
    FOREIGN KEY (MaSV, MaHP, HocKy, NamHoc) REFERENCES DANGKY(MaSV, MaHP, HocKy, NamHoc) ON DELETE CASCADE
);

-- [Bảng 8] TAIKHOAN 
CREATE TABLE TAIKHOAN (
    TenDangNhap VARCHAR(20) PRIMARY KEY,
    MatKhau VARBINARY(64) NOT NULL, -- Lưu Hash SHA2_256
    VaiTro NVARCHAR(20),
    MaSV VARCHAR(20) NULL,
    MaGV VARCHAR(20) NULL,
    TrangThai BIT DEFAULT 1,
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV),
    FOREIGN KEY (MaGV) REFERENCES GIANGVIEN(MaGV),
    CONSTRAINT CK_TAIKHOAN CHECK (
        (VaiTro = N'SV' AND MaSV IS NOT NULL AND MaGV IS NULL) OR
        (VaiTro = N'GV' AND MaGV IS NOT NULL AND MaSV IS NULL) OR
        (VaiTro = N'ADMIN')
    )
);

-- [Bảng 9] PHANCONG
CREATE TABLE PHANCONG (
    MaGV VARCHAR(20) NOT NULL,
    MaHP VARCHAR(20) NOT NULL,
    MaLop VARCHAR(20) NOT NULL,
    HocKy INT NOT NULL,
    NamHoc NVARCHAR(20) NOT NULL,
    PhongHoc NVARCHAR(50),
    PRIMARY KEY (MaGV, MaHP, MaLop, HocKy, NamHoc),
    CONSTRAINT FK_PC_GV FOREIGN KEY (MaGV) REFERENCES GIANGVIEN(MaGV) ON DELETE CASCADE,
    CONSTRAINT FK_PC_HP FOREIGN KEY (MaHP) REFERENCES HOCPHAN(MaHP) ON DELETE CASCADE,
    CONSTRAINT FK_PC_LOP FOREIGN KEY (MaLop) REFERENCES LOPHOC(MaLop) ON DELETE CASCADE
);
GO
--3.Index

--KHOA
CREATE NONCLUSTERED INDEX IDX_KHOA_TenKhoa ON KHOA(TenKhoa);

--GIANGVIEN
CREATE NONCLUSTERED INDEX IDX_GIANGVIEN_MaKhoa ON GIANGVIEN(MaKhoa);
CREATE NONCLUSTERED INDEX IDX_GIANGVIEN_HoTen ON GIANGVIEN(HoTen);
ALTER TABLE GIANGVIEN ADD CONSTRAINT UQ_Email UNIQUE(Email); 

--LOPHOC
CREATE NONCLUSTERED INDEX IDX_LOPHOC_MaKhoa ON LOPHOC(MaKhoa);
CREATE NONCLUSTERED INDEX IDX_LOPHOC_CoVanHocTap ON LOPHOC(CoVanHocTap);

--SINHVIEN
CREATE NONCLUSTERED INDEX IDX_SINHVIEN_MaLop ON SINHVIEN(MaLop);
CREATE NONCLUSTERED INDEX IDX_SINHVIEN_HoTen ON SINHVIEN(HoTen);

--HOCPHAN
CREATE NONCLUSTERED INDEX IDX_HOCPHAN_TenHP ON HOCPHAN(TenHP);
CREATE NONCLUSTERED INDEX IDX_HOCPHAN_MaKhoa ON HOCPHAN(MaKhoa);

--DANGKY
CREATE NONCLUSTERED INDEX IDX_DANGKY_MaSV ON DANGKY(MaSV);
CREATE NONCLUSTERED INDEX IDX_DANGKY_MaHP ON DANGKY(MaHP);
CREATE NONCLUSTERED INDEX IDX_DANGKY_HocKy_NamHoc ON DANGKY(HocKy, NamHoc);

--DIEM
CREATE NONCLUSTERED INDEX IDX_DIEM_MaSV ON DIEM(MaSV);
CREATE NONCLUSTERED INDEX IDX_DIEM_MaHP ON DIEM(MaHP);

--TAIKHOAN
CREATE NONCLUSTERED INDEX IDX_TAIKHOAN_VaiTro ON TAIKHOAN(VaiTro);
GO
CREATE NONCLUSTERED INDEX IDX_TAIKHOAN_LOGIN ON TAIKHOAN(TenDangNhap, MatKhau);
Go
--4.View

--VIEW SINH VIÊN FULL
CREATE OR ALTER VIEW VIEW_SinhVien_FullInfo
AS
SELECT
    sv.MaSV,
    sv.HoTen,
    sv.GioiTinh,
    sv.NgaySinh,
    sv.SDT,
    sv.DiaChi,
    sv.NamThu,
    sv.KhoaHoc,
    l.MaLop,
    l.TenLop,
    l.ChuyenNganh,
    k.MaKhoa,
    k.TenKhoa
FROM SINHVIEN sv
JOIN LOPHOC l ON sv.MaLop = l.MaLop
JOIN KHOA k ON l.MaKhoa = k.MaKhoa;
go
--VIEW BẢNG ĐIỂM
CREATE OR ALTER VIEW VIEW_BangDiem_Full
AS
SELECT 
    sv.MaSV,
    sv.HoTen,
    sv.MaLop AS MaLopSV,

    hp.MaHP,
    hp.TenHP,
    hp.TinChi,

    d.HocKy,
    d.NamHoc,

    d.DiemChuyenCan,
    d.DiemBaiTap,
    d.DiemGiuaKy,
    d.DiemCuoiKy,

    d.DiemTongKet, 

    pc.MaGV,

    CASE 
        WHEN d.DiemTongKet >= 8.5 THEN N'Giỏi'
        WHEN d.DiemTongKet >= 7 THEN N'Khá'
        WHEN d.DiemTongKet >= 5 THEN N'Trung bình'
        ELSE N'Yếu'
    END AS XepLoai

FROM DIEM d
JOIN SINHVIEN sv ON d.MaSV = sv.MaSV
JOIN HOCPHAN hp ON d.MaHP = hp.MaHP
OUTER APPLY (
    SELECT TOP 1 *
    FROM PHANCONG pc
    WHERE pc.MaHP = d.MaHP
      AND pc.HocKy = d.HocKy
      AND pc.NamHoc = d.NamHoc
      AND pc.MaLop = sv.MaLop
) pc;
GO
--VIEW GIẢNG VIÊN
CREATE OR ALTER VIEW VIEW_GiangVien_FullInfo
AS
SELECT
    gv.MaGV,
    gv.HoTen,
    gv.GioiTinh,
    gv.Email,
    gv.DiaChi,
    k.MaKhoa,
    k.TenKhoa
FROM GIANGVIEN gv
JOIN KHOA k ON gv.MaKhoa = k.MaKhoa;
go
--VIEW LỚP HỌC
CREATE OR ALTER VIEW VIEW_LopHoc_FullInfo
AS
SELECT
    l.MaLop,
    l.TenLop,
    l.ChuyenNganh,
    gv.HoTen AS TenCoVan,
    k.MaKhoa,
    k.TenKhoa
FROM LOPHOC l
LEFT JOIN GIANGVIEN gv ON l.CoVanHocTap = gv.MaGV
JOIN KHOA k ON l.MaKhoa = k.MaKhoa;
go
--VIEW TÀI KHOẢN
CREATE OR ALTER VIEW VIEW_TaiKhoan_FullInfo
AS
SELECT
    tk.TenDangNhap,
    tk.VaiTro,
    COALESCE(sv.HoTen, gv.HoTen, N'Admin') AS TenNguoiDung
FROM TAIKHOAN tk
LEFT JOIN SINHVIEN sv ON tk.MaSV = sv.MaSV
LEFT JOIN GIANGVIEN gv ON tk.MaGV = gv.MaGV;
go
--VIEW THỐNG KÊ LỚP
CREATE OR ALTER VIEW VIEW_ThongKeTheoLop
AS
SELECT 
    l.MaLop,
    l.TenLop,
    COUNT(sv.MaSV) AS SoLuongSinhVien,
    k.TenKhoa
FROM LOPHOC l
LEFT JOIN SINHVIEN sv ON l.MaLop = sv.MaLop
JOIN KHOA k ON l.MaKhoa = k.MaKhoa
GROUP BY l.MaLop, l.TenLop, k.TenKhoa;
go
--VIEW ĐIỂM TRUNG BÌNH
CREATE OR ALTER VIEW VIEW_DiemTrungBinh
AS
SELECT
    sv.MaSV,
    sv.HoTen,
    ROUND(AVG(d.DiemTongKet), 2) AS DiemTB
FROM SINHVIEN sv
LEFT JOIN DIEM d ON sv.MaSV = d.MaSV
GROUP BY sv.MaSV, sv.HoTen;
go 
--

CREATE OR ALTER VIEW VIEW_BaoCaoSinhVien
AS
SELECT 
    sv.MaSV,
    sv.HoTen,
    sv.GioiTinh,
    sv.NgaySinh,
    sv.SDT,
    sv.DiaChi,
    sv.NamThu,
    sv.KhoaHoc,
    l.MaLop,
    l.TenLop,
    l.ChuyenNganh
FROM SINHVIEN sv
LEFT JOIN LOPHOC l ON sv.MaLop = l.MaLop;
go 

--5. STORED PROCEDURES

-- SINH VIÊN
-- [1]XEM DANH SÁCH SINH VIÊN
CREATE OR ALTER PROCEDURE spXemSinhVien
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * FROM VIEW_SinhVien_FullInfo;
END;
GO

-- [2] THÊM SINH VIÊN
CREATE OR ALTER PROCEDURE spThemSinhVien 
    @MaSV VARCHAR(20),
    @HoTen NVARCHAR(100),
    @GioiTinh NVARCHAR(10),
    @NgaySinh DATE,
    @MaLop VARCHAR(20),
    @SDT VARCHAR(15),
    @DiaChi NVARCHAR(200),
    @NamThu INT,
    @KhoaHoc NVARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        INSERT INTO SINHVIEN 
        VALUES (@MaSV, @HoTen, @GioiTinh, @NgaySinh, @MaLop, @SDT, @DiaChi, @NamThu, @KhoaHoc);

        INSERT INTO TAIKHOAN 
        VALUES (
            @MaSV,
            HASHBYTES('SHA2_256', CAST(@MaSV AS NVARCHAR(MAX))),
            N'SV',
            @MaSV,
            NULL,
            1
        );

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END;
GO

-- [3] SỬA SINH VIÊN
CREATE OR ALTER PROCEDURE spSuaSinhVien
    @MaSV VARCHAR(20),
    @HoTen NVARCHAR(100),
    @GioiTinh NVARCHAR(10),
    @NgaySinh DATE,
    @MaLop VARCHAR(20),
    @SDT VARCHAR(15),
    @DiaChi NVARCHAR(200),
    @NamThu INT,
    @KhoaHoc NVARCHAR(20)
AS
BEGIN
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM SINHVIEN WHERE MaSV = @MaSV)
            THROW 50000, N'Mã sinh viên không tồn tại', 1;

        UPDATE SINHVIEN
        SET HoTen=@HoTen, GioiTinh=@GioiTinh, NgaySinh=@NgaySinh,
            MaLop=@MaLop, SDT=@SDT, DiaChi=@DiaChi,
            NamThu=@NamThu, KhoaHoc=@KhoaHoc
        WHERE MaSV=@MaSV;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO

-- [4] XÓA SINH VIÊN
CREATE OR ALTER PROCEDURE spXoaSinhVien
    @MaSV VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        DELETE FROM SINHVIEN WHERE MaSV=@MaSV;
        -- KHÔNG cần xóa tài khoản nữa (trigger xử lý)

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END;
GO
--GIẢNG VIÊN
--[1] xem giảng viên
CREATE OR ALTER PROCEDURE spXemGiangVien
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * FROM VIEW_GiangVien_FullInfo;
END;
GO
--[2]thêm giảng viên 
CREATE OR ALTER PROCEDURE spThemGiangVien
    @MaGV VARCHAR(20),
    @HoTen NVARCHAR(100),
    @GioiTinh NVARCHAR(10),
    @DiaChi NVARCHAR(200),
    @Email VARCHAR(100),
    @MaKhoa VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        INSERT INTO GIANGVIEN 
        VALUES (@MaGV, @HoTen, @GioiTinh, @DiaChi, @Email, @MaKhoa);

        INSERT INTO TAIKHOAN 
        VALUES (
            @MaGV,
            HASHBYTES('SHA2_256', CAST(@MaGV AS NVARCHAR(MAX))),
            N'GV',
            NULL,
            @MaGV,
            1
        );

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END;
GO
-- [3]SỬA GIẢNG VIÊN
CREATE OR ALTER PROCEDURE spSuaGiangVien
    @MaGV     VARCHAR(20),
    @HoTen    NVARCHAR(100),
    @GioiTinh NVARCHAR(10),
    @DiaChi   NVARCHAR(200),
    @Email    VARCHAR(100),
    @MaKhoa   VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM GIANGVIEN WHERE MaGV = @MaGV)
        BEGIN
            RAISERROR(N'Mã giảng viên không tồn tại.', 16, 1);
            RETURN;
        END

        IF NOT EXISTS (SELECT 1 FROM KHOA WHERE MaKhoa = @MaKhoa)
        BEGIN
            RAISERROR(N'Mã khoa không tồn tại.', 16, 1);
            RETURN;
        END

        UPDATE GIANGVIEN
        SET HoTen    = @HoTen,
            GioiTinh = @GioiTinh,
            DiaChi   = @DiaChi,
            Email    = @Email,
            MaKhoa   = @MaKhoa
        WHERE MaGV = @MaGV;
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO

-- [4] XÓA GIẢNG VIÊN
CREATE OR ALTER PROCEDURE spXoaGiangVien
    @MaGV VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION

        IF NOT EXISTS (SELECT 1 FROM GIANGVIEN WHERE MaGV = @MaGV)
        BEGIN
            RAISERROR(N'Mã giảng viên không tồn tại.', 16, 1);
            ROLLBACK; RETURN;
        END

        -- Gỡ cố vấn học tập trước khi xóa
        UPDATE LOPHOC SET CoVanHocTap = NULL WHERE CoVanHocTap = @MaGV;

        DELETE FROM TAIKHOAN WHERE MaGV = @MaGV;
        -- PHANCONG tự xóa CASCADE
        DELETE FROM GIANGVIEN WHERE MaGV = @MaGV;

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO

-- HỌC PHẦN
--[1]xem học phần 
CREATE OR ALTER PROCEDURE spXemHocPhan
AS
BEGIN
    SELECT hp.MaHP, hp.TenHP, hp.TinChi, k.TenKhoa
    FROM HOCPHAN hp
    LEFT JOIN KHOA k ON hp.MaKhoa = k.MaKhoa;
END;
GO
--[2] thêm học phần 
CREATE OR ALTER PROCEDURE spThemHocPhan
    @MaHP   VARCHAR(20),
    @TenHP  NVARCHAR(100),
    @TinChi INT,
    @MaKhoa VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION

        IF EXISTS (SELECT 1 FROM HOCPHAN WHERE MaHP = @MaHP)
        BEGIN
            RAISERROR(N'Mã học phần đã tồn tại.',16,1)
            ROLLBACK; RETURN;
        END

        IF @TinChi <= 0
        BEGIN
            RAISERROR(N'Tín chỉ phải > 0.',16,1)
            ROLLBACK; RETURN;
        END

        IF NOT EXISTS (SELECT 1 FROM KHOA WHERE MaKhoa = @MaKhoa)
        BEGIN
            RAISERROR(N'Mã khoa không tồn tại.',16,1)
            ROLLBACK; RETURN;
        END

        INSERT INTO HOCPHAN(MaHP, TenHP, TinChi, MaKhoa)
        VALUES(@MaHP, @TenHP, @TinChi, @MaKhoa)

        COMMIT
    END TRY
    BEGIN CATCH
        ROLLBACK
        DECLARE @ErrMsg NVARCHAR(500)
        SET @ErrMsg = ERROR_MESSAGE()
        RAISERROR(@ErrMsg,16,1)
    END CATCH
END;
GO
--[3] sửa học phần 
    CREATE OR ALTER PROCEDURE spSuaHocPhan
    @MaHP   VARCHAR(20),
    @TenHP  NVARCHAR(100),
    @TinChi INT,
    @MaKhoa VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM HOCPHAN WHERE MaHP = @MaHP)
        BEGIN
            RAISERROR(N'Mã học phần không tồn tại.',16,1)
            RETURN;
        END

        IF @TinChi <= 0
        BEGIN
            RAISERROR(N'Tín chỉ phải > 0.',16,1)
            RETURN;
        END

        UPDATE HOCPHAN
        SET TenHP = @TenHP,
            TinChi = @TinChi,
            MaKhoa = @MaKhoa
        WHERE MaHP = @MaHP
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(500)
        SET @ErrMsg = ERROR_MESSAGE()
        RAISERROR(@ErrMsg,16,1)
    END CATCH
END;
GO
--[4] xóa học phần 
CREATE OR ALTER PROCEDURE spXoaHocPhan
    @MaHP VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION

        IF NOT EXISTS (SELECT 1 FROM HOCPHAN WHERE MaHP = @MaHP)
        BEGIN
            RAISERROR(N'Mã học phần không tồn tại.',16,1)
            ROLLBACK; RETURN;
        END

        DELETE FROM DIEM WHERE MaHP = @MaHP
        DELETE FROM DANGKY WHERE MaHP = @MaHP
        DELETE FROM PHANCONG WHERE MaHP = @MaHP

        DELETE FROM HOCPHAN WHERE MaHP = @MaHP

        COMMIT
    END TRY
    BEGIN CATCH
        ROLLBACK
        DECLARE @ErrMsg NVARCHAR(500)
        SET @ErrMsg = ERROR_MESSAGE()
        RAISERROR(@ErrMsg,16,1)
    END CATCH
END
go

--ĐĂNG KÝ HỌC
-- [1] đăng ký học
CREATE OR ALTER PROCEDURE spDangKyHoc
    @MaSV VARCHAR(20),
    @MaHP VARCHAR(20),
    @HocKy INT,
    @NamHoc NVARCHAR(20)
AS
BEGIN
    BEGIN TRY
        -- Check tồn tại SV
        IF NOT EXISTS (SELECT 1 FROM SINHVIEN WHERE MaSV=@MaSV)
        BEGIN
            RAISERROR(N'Sinh viên không tồn tại.',16,1)
            RETURN
        END

        -- Check tồn tại học phần
        IF NOT EXISTS (SELECT 1 FROM HOCPHAN WHERE MaHP=@MaHP)
        BEGIN
            RAISERROR(N'Học phần không tồn tại.',16,1)
            RETURN
        END

        -- Check trùng
        IF EXISTS (
            SELECT 1 FROM DANGKY
            WHERE MaSV=@MaSV AND MaHP=@MaHP 
              AND HocKy=@HocKy AND NamHoc=@NamHoc
        )
        BEGIN
            RAISERROR(N'Đã đăng ký rồi.',16,1)
            RETURN
        END

        INSERT INTO DANGKY VALUES (@MaSV, @MaHP, @HocKy, @NamHoc)

    END TRY
    BEGIN CATCH
        DECLARE @Err NVARCHAR(500)=ERROR_MESSAGE()
        RAISERROR(@Err,16,1)
    END CATCH
END;
GO
  -- [2] HỦY ĐĂNG KÝ
CREATE OR ALTER PROCEDURE spHuyDangKy
    @MaSV   VARCHAR(20),
    @MaHP   VARCHAR(20),
    @HocKy  INT,
    @NamHoc NVARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION

        IF NOT EXISTS (
            SELECT 1 FROM DANGKY
            WHERE MaSV = @MaSV AND MaHP = @MaHP
              AND HocKy = @HocKy AND NamHoc = @NamHoc
        )
        BEGIN
            RAISERROR(N'Không tìm thấy đăng ký để hủy.', 16, 1);
            ROLLBACK; RETURN;
        END
        DELETE FROM DIEM
        WHERE MaSV = @MaSV AND MaHP = @MaHP
          AND HocKy = @HocKy AND NamHoc = @NamHoc;

        DELETE FROM DANGKY
        WHERE MaSV = @MaSV AND MaHP = @MaHP
          AND HocKy = @HocKy AND NamHoc = @NamHoc;

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO

-- [3] XEM ĐĂNG KÝ THEO SINH VIÊN
CREATE OR ALTER PROCEDURE spXemDangKyTheoSV
    @MaSV VARCHAR(20)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM SINHVIEN WHERE MaSV = @MaSV)
    BEGIN
        RAISERROR(N'Mã sinh viên không tồn tại.', 16, 1);
        RETURN;
    END

    SELECT
        dk.MaSV,
        sv.HoTen,
        dk.MaHP,
        hp.TenHP,
        hp.TinChi,
        dk.HocKy,
        dk.NamHoc
    FROM DANGKY dk
    JOIN SINHVIEN sv ON dk.MaSV = sv.MaSV
    JOIN HOCPHAN  hp ON dk.MaHP = hp.MaHP
    WHERE dk.MaSV = @MaSV
    ORDER BY dk.NamHoc, dk.HocKy;
END;
GO


-- 5. ĐIỂM

-- [1] NHẬP ĐIỂM
CREATE OR ALTER PROCEDURE spNhapDiem
    @MaSV VARCHAR(20),
    @MaHP VARCHAR(20),
    @HocKy INT,
    @NamHoc NVARCHAR(20),
    @DiemCC DECIMAL(4,2),
    @DiemBT DECIMAL(4,2),
    @DiemGK DECIMAL(4,2),
    @DiemCK DECIMAL(4,2)
AS
BEGIN
    BEGIN TRY
        -- Check đăng ký
        IF NOT EXISTS (
            SELECT 1 FROM DANGKY
            WHERE MaSV=@MaSV AND MaHP=@MaHP 
              AND HocKy=@HocKy AND NamHoc=@NamHoc
        )
        BEGIN
            RAISERROR(N'Sinh viên chưa đăng ký học phần này.',16,1)
            RETURN
        END

        -- Check đã có điểm chưa
        IF EXISTS (
            SELECT 1 FROM DIEM
            WHERE MaSV=@MaSV AND MaHP=@MaHP 
              AND HocKy=@HocKy AND NamHoc=@NamHoc
        )
        BEGIN
            RAISERROR(N'Đã tồn tại điểm, dùng chức năng sửa.',16,1)
            RETURN
        END

        INSERT INTO DIEM 
        VALUES (@MaSV, @MaHP, @HocKy, @NamHoc, @DiemCC, @DiemBT, @DiemGK, @DiemCK)

    END TRY
    BEGIN CATCH
        DECLARE @Err NVARCHAR(500)=ERROR_MESSAGE()
        RAISERROR(@Err,16,1)
    END CATCH
END;
GO
-- [2] SỬA ĐIỂM
CREATE OR ALTER PROCEDURE spSuaDiem
    @MaSV    VARCHAR(20),
    @MaHP    VARCHAR(20),
    @HocKy   INT,
    @NamHoc  NVARCHAR(20),
    @DiemCC  DECIMAL(4,2),
    @DiemBT  DECIMAL(4,2),
    @DiemGK  DECIMAL(4,2),
    @DiemCK  DECIMAL(4,2)
AS
BEGIN
    BEGIN TRY
        IF NOT EXISTS (
            SELECT 1 FROM DIEM
            WHERE MaSV = @MaSV AND MaHP = @MaHP
              AND HocKy = @HocKy AND NamHoc = @NamHoc
        )
        BEGIN
            RAISERROR(N'Không tìm thấy bản ghi điểm để sửa.', 16, 1);
            RETURN;
        END

        UPDATE DIEM
        SET DiemChuyenCan = @DiemCC,
            DiemBaiTap    = @DiemBT,
            DiemGiuaKy    = @DiemGK,
            DiemCuoiKy    = @DiemCK
        WHERE MaSV = @MaSV AND MaHP = @MaHP
          AND HocKy = @HocKy AND NamHoc = @NamHoc;
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO

-- [3] XEM BẢNG ĐIỂM
CREATE OR ALTER PROCEDURE spXemBangDiem
    @MaSV VARCHAR(20) = NULL
AS
BEGIN
    IF @MaSV IS NOT NULL AND NOT EXISTS (SELECT 1 FROM SINHVIEN WHERE MaSV = @MaSV)
    BEGIN
        RAISERROR(N'Mã sinh viên không tồn tại.', 16, 1);
        RETURN;
    END

    SELECT *
    FROM VIEW_BangDiem_Full
    WHERE (@MaSV IS NULL OR MaSV = @MaSV)
    ORDER BY MaSV, NamHoc, HocKy;
END;
GO


--TÀI KHOẢN
--[1] login
CREATE OR ALTER PROCEDURE spLogin
    @TenDangNhap VARCHAR(20),
    @MatKhau NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        tk.TenDangNhap,
        tk.VaiTro,
        tk.MaSV,
        tk.MaGV,
        COALESCE(sv.HoTen, gv.HoTen) AS HoTen,

        CASE 
            WHEN tk.VaiTro = 'SV' THEN lh.MaKhoa
            WHEN tk.VaiTro = 'GV' THEN gv.MaKhoa
            ELSE NULL
        END AS MaKhoa

    FROM TAIKHOAN tk
    LEFT JOIN SINHVIEN sv ON tk.MaSV = sv.MaSV
    LEFT JOIN LOPHOC lh ON sv.MaLop = lh.MaLop
    LEFT JOIN GIANGVIEN gv ON tk.MaGV = gv.MaGV

    WHERE tk.TenDangNhap = @TenDangNhap
      AND tk.MatKhau = HASHBYTES('SHA2_256', @MatKhau)
      AND tk.TrangThai = 1;
END;

GO
  --[2] lấy thông tin user
CREATE OR ALTER PROCEDURE spGetUserInfo
    @TenDangNhap VARCHAR(20)
AS
BEGIN
    SELECT
        tk.TenDangNhap,
        tk.VaiTro,
        tk.MaSV,
        tk.MaGV,
        COALESCE(sv.HoTen, gv.HoTen, N'Quản trị viên') AS HoTen,
        COALESCE(sv.MaLop, gv.MaKhoa, N'ADMIN') AS MaKhoa -- Bổ sung để fix lỗi C#
    FROM TAIKHOAN tk
    LEFT JOIN SINHVIEN sv ON tk.MaSV = sv.MaSV
    LEFT JOIN GIANGVIEN gv ON tk.MaGV = gv.MaGV
    WHERE tk.TenDangNhap = @TenDangNhap;
END;
GO

-- [3] thêm tài khoản 
CREATE OR ALTER PROCEDURE spThemTaiKhoan
    @TenDangNhap VARCHAR(20),
    @MatKhau     NVARCHAR(100),
    @VaiTro      NVARCHAR(20),
    @MaSV        VARCHAR(20) = NULL,
    @MaGV        VARCHAR(20) = NULL
AS
BEGIN
    BEGIN TRY
        IF EXISTS (SELECT 1 FROM TAIKHOAN WHERE TenDangNhap = @TenDangNhap)
        BEGIN
            RAISERROR(N'Tên đăng nhập đã tồn tại.', 16, 1);
            RETURN;
        END

        INSERT INTO TAIKHOAN (TenDangNhap, MatKhau, VaiTro, MaSV, MaGV, TrangThai)
        VALUES (
            @TenDangNhap,
            HASHBYTES('SHA2_256', CAST(@MatKhau AS NVARCHAR(MAX))),
            @VaiTro,
            @MaSV,
            @MaGV,
            1
        );
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO
  -- [4] đổi mật khẩu 
CREATE OR ALTER PROCEDURE spDoiMatKhau
    @TenDangNhap VARCHAR(20),
    @MatKhauMoi  NVARCHAR(100)
AS
BEGIN
    UPDATE TAIKHOAN
SET MatKhau = HASHBYTES('SHA2_256', @MatKhauMoi)
WHERE TenDangNhap = @TenDangNhap
END;
GO
--[5] xóa tài khoản 
  CREATE OR ALTER PROCEDURE spXoaTaiKhoan
    @TenDangNhap VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION
            IF NOT EXISTS (SELECT 1 FROM TAIKHOAN WHERE TenDangNhap = @TenDangNhap)
            BEGIN
                RAISERROR(N'Tên đăng nhập không tồn tại.', 16, 1);
                ROLLBACK; RETURN;
            END

            DELETE FROM TAIKHOAN WHERE TenDangNhap = @TenDangNhap;
            
            SELECT N'Xóa tài khoản thành công' AS Message;
        COMMIT;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK;
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO

-- PHÂN CÔNG
--[1] xem phân côg theo giảng viên 
  CREATE OR ALTER PROCEDURE spXemPhanCongTheoGV
    @MaGV VARCHAR(20)
AS
BEGIN
    SELECT 
        pc.MaLop,
        lh.TenLop,
        hp.MaHP,
        hp.TenHP,
        hp.TinChi,
        pc.HocKy,
        pc.NamHoc,
        pc.PhongHoc
    FROM PHANCONG pc
    JOIN HOCPHAN hp ON pc.MaHP = hp.MaHP
    JOIN LOPHOC lh ON pc.MaLop = lh.MaLop
    WHERE pc.MaGV = @MaGV
END
go
--[2] phân công 
CREATE OR ALTER PROCEDURE spPhanCong
    @MaGV VARCHAR(20),
    @MaHP VARCHAR(20),
    @MaLop VARCHAR(20),
    @HocKy INT,
    @NamHoc NVARCHAR(20)
AS
BEGIN
    BEGIN TRY
        -- Check GV
        IF NOT EXISTS (SELECT 1 FROM GIANGVIEN WHERE MaGV=@MaGV)
        BEGIN
            RAISERROR(N'Giảng viên không tồn tại.',16,1)
            RETURN
        END

        -- Check HP
        IF NOT EXISTS (SELECT 1 FROM HOCPHAN WHERE MaHP=@MaHP)
        BEGIN
            RAISERROR(N'Học phần không tồn tại.',16,1)
            RETURN
        END

        -- Check lớp
        IF NOT EXISTS (SELECT 1 FROM LOPHOC WHERE MaLop=@MaLop)
        BEGIN
            RAISERROR(N'Lớp không tồn tại.',16,1)
            RETURN
        END

        -- Check trùng
        IF EXISTS (
            SELECT 1 FROM PHANCONG
            WHERE MaGV=@MaGV AND MaHP=@MaHP 
              AND MaLop=@MaLop AND HocKy=@HocKy AND NamHoc=@NamHoc
        )
        BEGIN
            RAISERROR(N'Phân công đã tồn tại.',16,1)
            RETURN
        END

        INSERT INTO PHANCONG
        VALUES (@MaGV, @MaHP, @MaLop, @HocKy, @NamHoc, NULL)

    END TRY
    BEGIN CATCH
        DECLARE @Err NVARCHAR(500)=ERROR_MESSAGE()
        RAISERROR(@Err,16,1)
    END CATCH
END;
GO
--[3] cập nhật phong học
  CREATE OR ALTER PROCEDURE spCapPhong
    @MaGV     VARCHAR(20),
    @MaHP     VARCHAR(20),
    @MaLop    VARCHAR(20),
    @HocKy    INT,
    @NamHoc   NVARCHAR(20),
    @PhongHoc NVARCHAR(50)
AS
BEGIN
    BEGIN TRY
        IF NOT EXISTS (
            SELECT 1 FROM PHANCONG
            WHERE MaGV = @MaGV AND MaHP = @MaHP AND MaLop = @MaLop
              AND HocKy = @HocKy AND NamHoc = @NamHoc
        )
        BEGIN
            RAISERROR(N'Không tìm thấy phân công để cập nhật phòng.', 16, 1);
            RETURN;
        END

        UPDATE PHANCONG
        SET PhongHoc = @PhongHoc
        WHERE MaGV = @MaGV AND MaHP = @MaHP AND MaLop = @MaLop
          AND HocKy = @HocKy AND NamHoc = @NamHoc;
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(500) = ERROR_MESSAGE();
        RAISERROR(@ErrMsg, 16, 1);
    END CATCH
END;
GO


-- LỚP HỌC
-- danh sách lớp 
CREATE OR ALTER PROCEDURE spXemLopHoc
AS
BEGIN
    SELECT l.MaLop, l.TenLop, k.TenKhoa
    FROM LOPHOC l
    JOIN KHOA k ON l.MaKhoa = k.MaKhoa;
END;
GO

--6.Trigger
-- Trigger Khóa Khoa
CREATE OR ALTER TRIGGER trg_KhongXoaKhoa
ON KHOA
INSTEAD OF DELETE
AS
BEGIN
    IF EXISTS (SELECT 1 FROM LOPHOC l JOIN deleted d ON l.MaKhoa = d.MaKhoa)
    BEGIN
        RAISERROR(N'Không thể xóa Khoa vì còn Lớp học!',16,1)
        RETURN
    END
    IF EXISTS (SELECT 1 FROM GIANGVIEN g JOIN deleted d ON g.MaKhoa = d.MaKhoa)
    BEGIN
        RAISERROR(N'Không thể xóa Khoa vì còn Giảng viên!',16,1)
        RETURN
    END
    IF EXISTS (SELECT 1 FROM HOCPHAN h JOIN deleted d ON h.MaKhoa = d.MaKhoa)
    BEGIN
        RAISERROR(N'Không thể xóa Khoa vì còn Học phần!',16,1)
        RETURN
    END
    DELETE FROM KHOA WHERE MaKhoa IN (SELECT MaKhoa FROM deleted)
END;
GO

-- Trigger Xóa Sinh viên
CREATE OR ALTER TRIGGER trg_XoaSinhVien
ON SINHVIEN
AFTER DELETE
AS
BEGIN
    DELETE FROM TAIKHOAN WHERE MaSV IN (SELECT MaSV FROM deleted)
END;
GO
