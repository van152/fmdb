void __fastcall sub_14081DFC0(__int64 a1, char a2, int a3, int **a4)
{
  _QWORD *v4; // rdi
  __int64 v5; // r15
  __int64 *v6; // r12
  __int64 v7; // rax
  volatile signed __int32 *v8; // rcx
  volatile signed __int32 *v9; // rsi
  volatile signed __int32 *v10; // rsi
  __int64 v11; // rdx
  __int64 v12; // rdi
  volatile signed __int32 *v13; // rdx
  unsigned int v14; // esi
  _QWORD *v15; // r14
  _QWORD *v16; // r15
  bool v17; // r12
  bool v18; // zf
  __int64 *v19; // r12
  __int64 v20; // rax
  __int64 v21; // rdi
  __int64 v22; // rdi
  __int64 v23; // rbx
  __int64 v24; // r14
  __int64 v25; // r13
  __int64 v26; // rsi
  __int64 v27; // rdi
  unsigned int v28; // eax
  __int64 *v29; // rax
  __int64 *v30; // rax
  __int64 *v31; // rdx
  __int64 *v32; // rcx
  __int64 *v33; // rdi
  volatile signed __int32 *v34; // rcx
  _QWORD *v35; // rbx
  volatile signed __int32 **v36; // rax
  volatile signed __int32 *v37; // rax
  int v38; // ebx
  __int64 v39; // rax
  __int64 v40; // rdi
  volatile signed __int32 *v41; // rsi
  __int64 v42; // rdx
  int v43; // eax
  __int64 v44; // rax
  int v45; // r12d
  unsigned int v46; // eax
  int v47; // r12d
  int v48; // eax
  int v49; // ecx
  int v50; // edi
  __int64 v51; // r8
  __int64 v52; // r13
  __int64 v53; // rsi
  volatile signed __int32 *v54; // rcx
  __int64 v55; // rax
  __int64 v56; // rdx
  int v57; // ecx
  _DWORD *v58; // rax
  __int64 v59; // rcx
  int v60; // eax
  char v61; // di
  void (__fastcall ***v62)(_QWORD, __int64); // rcx
  volatile signed __int32 *v63; // rdi
  __int64 v64; // rbx
  __int64 v65; // rsi
  int v66; // esi
  unsigned int v67; // eax
  int v68; // esi
  int v69; // eax
  int v70; // ebx
  int v71; // edx
  __int64 v72; // rcx
  unsigned int v73; // esi
  __int64 v74; // r14
  int v75; // edi
  __int64 v76; // rsi
  __int64 v77; // r14
  __int64 v78; // rax
  volatile signed __int32 *v79; // rcx
  __int64 v80; // rcx
  __int64 v81; // rbx
  __int64 *v83; // [rsp+30h] [rbp-50h]
  __int64 v84; // [rsp+38h] [rbp-48h]
  __int64 v86; // [rsp+48h] [rbp-38h] BYREF
  __int64 v87; // [rsp+50h] [rbp-30h]
  int v88; // [rsp+5Ch] [rbp-24h]
  __int64 v89; // [rsp+60h] [rbp-20h]
  volatile signed __int32 *v90; // [rsp+68h] [rbp-18h] BYREF
  int v91; // [rsp+74h] [rbp-Ch]
  char v92; // [rsp+7Eh] [rbp-2h] BYREF
  char v93; // [rsp+7Fh] [rbp-1h]
  __int128 v94; // [rsp+80h] [rbp+0h] BYREF
  __int64 v95; // [rsp+90h] [rbp+10h]

  v95 = -2;
  v93 = a2;
  v4 = *(_QWORD **)(a1 + 16);
  if ( v4 != nullptr )
  {
    v5 = a1;
    v6 = (__int64 *)(a1 + 8);
    if ( (__int64 *)(a1 + 8) != &qword_141B59EE0 )
    {
      v7 = *v6;
      v8 = (volatile signed __int32 *)(*v6 - 4);
      if ( *v6 == 0 )
        v8 = nullptr;
      v9 = (volatile signed __int32 *)(qword_141B59EE0 - 4);
      if ( qword_141B59EE0 != 0 )
      {
        if ( v7 != 0 && _InterlockedDecrement(v8) == 0 )
          sub_1412EC9A0((__int64)v8);
        *v6 = 0;
        _InterlockedIncrement(v9);
        v10 = v9 + 1;
      }
      else
      {
        if ( v7 != 0 && _InterlockedDecrement(v8) == 0 )
          sub_1412EC9A0((__int64)v8);
        v10 = nullptr;
      }
      *(_QWORD *)(v5 + 8) = v10;
      v4 = *(_QWORD **)(v5 + 16);
    }
    v11 = v4[1];
    if ( *v4 == v11 )
    {
LABEL_175:
      sub_14081D260(v4);
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(&unk_141B59A68);
          sub_141751048(sub_1407E4B20);
          sub_141750EA0(&dword_141B59AA8);
        }
      }
      if ( byte_141B59A9C != 0
        && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
        && (v81 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
      {
        MEMORY[0x1419475D8](v81 + 32, (char *)v4 - *(unsigned int *)(v81 + 120));
        if ( (*(_BYTE *)(v81 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v81 + 64)) == 0)
          && *(_BYTE *)(v81 + 97) != 0 )
        {
          sub_1412D33C0(v81);
        }
      }
      else
      {
        MEMORY[0x141948990]((char *)v4 - (unsigned int)dword_141B59A98);
      }
LABEL_183:
      *(_QWORD *)(v5 + 16) = 0;
      return;
    }
    sub_1408200B0(*v4, v11, (v11 - *v4) >> 3);
    v84 = ***(_QWORD ***)(v5 + 16);
    v94 = 0;
    v12 = sub_1412EC810(264, 1024);
    *(_QWORD *)v12 = 0x40000000000LL;
    *(_BYTE *)(v12 + 8) = 0;
    v13 = (volatile signed __int32 *)v94;
    if ( (_QWORD)v94 != 0 )
    {
      v14 = 1024;
      if ( SHIDWORD(v94) < 1024 )
        v14 = HIDWORD(v94);
      if ( SHIDWORD(v94) > 0 )
      {
        sub_141758A00();
        *(_BYTE *)(v12 + 8 + v14) = 0;
        v13 = (volatile signed __int32 *)v94;
      }
      HIDWORD(v94) = v14;
      if ( v13 == (volatile signed __int32 *)v12 )
      {
LABEL_26:
        v83 = v6;
        v87 = v5;
        v15 = *(_QWORD **)v84;
        v16 = *(_QWORD **)(v84 + 8);
        v88 = -1;
        v17 = false;
        if ( v15 == v16 )
        {
LABEL_27:
          v18 = !v17;
          v5 = v87;
          v19 = v83;
          if ( v18 )
            goto LABEL_158;
          LODWORD(v20) = HIDWORD(v94);
          if ( HIDWORD(v94) == 0 )
            goto LABEL_158;
          v21 = v94 + 8;
          if ( SHIDWORD(v94) > 0 )
          {
            v20 = (unsigned int)(HIDWORD(v94) - 1);
            if ( *(char *)(v21 + v20) <= -65 )
              LODWORD(v20) = sub_1417584B0(v94 + 8, 0, (unsigned int)v20);
          }
          if ( (unsigned int)sub_140811DC0(v21, (unsigned int)v20) != 32 )
            goto LABEL_158;
          LODWORD(v22) = HIDWORD(v94);
          v23 = v94;
          v24 = v94 + 8;
          if ( SHIDWORD(v94) <= 0 )
          {
            if ( (_QWORD)v94 == 0 )
            {
              v66 = 0;
              goto LABEL_142;
            }
          }
          else
          {
            v22 = (unsigned int)(HIDWORD(v94) - 1);
            if ( *(char *)(v24 + v22) <= -65 )
              LODWORD(v22) = sub_1417584B0(v94 + 8, 0, (unsigned int)v22);
          }
          v66 = 0;
          if ( (int)v22 < *(_DWORD *)(v23 + 4) )
          {
            v67 = sub_140811DC0(v24, (unsigned int)v22);
            if ( v67 >= 0x80 )
            {
              v66 = 1;
              if ( v67 >= 0x800 )
              {
                v66 = 2;
                if ( v67 >= 0xD800 )
                {
                  v66 = -1;
                  if ( v67 - 1114112 >= 0xFFEFE000 )
                    v66 = (v67 < 0x10000) ^ 3;
                }
              }
            }
          }
LABEL_142:
          v68 = v22 + v66;
          v69 = HIDWORD(v94);
          v70 = (HIDWORD(v94) - 1) & ((HIDWORD(v94) - 1) >> 31);
          v71 = 0;
          if ( HIDWORD(v94) - 1 > 0 )
            v71 = HIDWORD(v94) - 1;
          if ( (int)v22 <= v70 )
            LODWORD(v22) = (HIDWORD(v94) - 1) & ((HIDWORD(v94) - 1) >> 31);
          if ( (int)v22 >= v71 )
            LODWORD(v22) = v71;
          if ( v68 > v70 )
            v70 = v68;
          if ( v70 >= v71 )
            v70 = v71;
          if ( v70 >= (int)v22 && SHIDWORD(v94) > 0 )
          {
            v72 = v94;
            if ( (_QWORD)v94 == 0 )
              goto LABEL_163;
            v73 = HIDWORD(v94) - (v70 + 1);
            if ( SHIDWORD(v94) > v70 + 1 )
            {
              v74 = v94 + (int)v22 + 8;
              sub_141758A00();
              *(_BYTE *)(v73 + v74) = 0;
              v69 = HIDWORD(v94);
              v72 = v94;
            }
            HIDWORD(v94) = v69 + ~v70 + v22;
            *(_BYTE *)(v72 + SHIDWORD(v94) + 8) = 0;
          }
LABEL_158:
          if ( (_QWORD)v94 != 0 )
          {
            v75 = HIDWORD(v94);
            if ( HIDWORD(v94) == -1 )
            {
              v75 = sub_141758DB0(v94 + 8);
              if ( v75 > 0 )
                goto LABEL_161;
            }
            else if ( SHIDWORD(v94) > 0 )
            {
LABEL_161:
              v76 = sub_1412EC810(264, (unsigned int)v75);
              *(_DWORD *)v76 = 0;
              v77 = v76 + 4;
              *(_DWORD *)(v76 + 4) = v75;
              sub_141758A00();
              *(_BYTE *)(v76 + (unsigned int)v75 + 8) = 0;
              _InterlockedIncrement((volatile signed __int32 *)v76);
              v19 = v83;
              goto LABEL_164;
            }
          }
LABEL_163:
          v77 = 0;
LABEL_164:
          v78 = *v19;
          if ( *v19 == v77 )
          {
            if ( v77 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v77 - 4)) == 0 )
              sub_1412EC9A0(v77 - 4);
          }
          else
          {
            v79 = (volatile signed __int32 *)(v78 - 4);
            if ( v78 != 0 && _InterlockedDecrement(v79) == 0 )
              sub_1412EC9A0((__int64)v79);
            *v19 = v77;
          }
          if ( *(_BYTE *)(v5 + 28) == 0xFF )
            *(_BYTE *)(v5 + 28) = *(_BYTE *)(v84 + 32);
          v80 = v94;
          if ( (_QWORD)v94 != 0 && _InterlockedDecrement((volatile signed __int32 *)v94) == 0 )
            sub_1412EC9A0(v80);
          v4 = *(_QWORD **)(v5 + 16);
          if ( v4 == nullptr )
            goto LABEL_183;
          goto LABEL_175;
        }
        while ( 1 )
        {
          while ( 1 )
          {
            v25 = *(_QWORD *)(*v15 + 16LL);
            if ( v25 != 0 )
              break;
            v36 = (volatile signed __int32 **)(*v15 + 8LL);
            v90 = nullptr;
            if ( &v90 != v36 )
            {
              v37 = *v36;
              if ( v37 != nullptr )
                _InterlockedIncrement(v37 - 1);
              v90 = v37;
            }
            v38 = HIDWORD(v94);
            v39 = v94;
            if ( (_QWORD)v94 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)v94);
            v89 = v39;
            sub_140806120(&v94, &v90);
            v40 = v94;
            v41 = (volatile signed __int32 *)v89;
            if ( *(_DWORD *)(v89 + 4) > *(_DWORD *)(v94 + 4) )
              v40 = v89;
            if ( v17 && v90 != nullptr )
            {
              v42 = *(unsigned int *)v90;
              if ( (_DWORD)v42 != 0 )
              {
                v43 = sub_1408103D0(v90 + 1, v42, 0);
                v41 = (volatile signed __int32 *)v89;
                if ( v43 == 32 )
                {
                  if ( v38 == 0 )
                    goto LABEL_73;
                  LODWORD(v44) = v38;
                  if ( v38 > 0 )
                  {
                    v44 = (unsigned int)(v38 - 1);
                    if ( *(char *)(v40 + 8 + v44) <= -65 )
                      LODWORD(v44) = sub_1417584B0(v40 + 8, 0, (unsigned int)v44);
                  }
                  if ( (unsigned int)sub_140811DC0(v40 + 8, (unsigned int)v44) == 32 )
                  {
LABEL_73:
                    v45 = 0;
                    if ( v40 != 0 && v38 < *(_DWORD *)(v40 + 4) )
                    {
                      v46 = sub_140811DC0(v40 + 8, (unsigned int)v38);
                      if ( v46 >= 0x80 )
                      {
                        v45 = 1;
                        if ( v46 >= 0x800 )
                        {
                          v45 = 2;
                          if ( v46 >= 0xD800 )
                          {
                            v45 = -1;
                            if ( v46 - 1114112 >= 0xFFEFE000 )
                              v45 = (v46 < 0x10000) ^ 3;
                          }
                        }
                      }
                    }
                    v47 = v38 + v45;
                    v48 = HIDWORD(v94);
                    v49 = HIDWORD(v94) - 1;
                    v50 = (HIDWORD(v94) - 1) & ((HIDWORD(v94) - 1) >> 31);
                    if ( HIDWORD(v94) - 1 <= 0 )
                      v49 = 0;
                    if ( v38 <= v50 )
                      v38 = (HIDWORD(v94) - 1) & ((HIDWORD(v94) - 1) >> 31);
                    if ( v38 >= v49 )
                      v38 = v49;
                    if ( v47 > v50 )
                      v50 = v47;
                    if ( v50 >= v49 )
                      v50 = v49;
                    if ( v50 >= v38 && SHIDWORD(v94) > 0 )
                    {
                      v51 = v94;
                      if ( (_QWORD)v94 != 0 )
                      {
                        if ( SHIDWORD(v94) > v50 + 1 )
                        {
                          v52 = v94 + v38 + 8;
                          v53 = (unsigned int)(HIDWORD(v94) - (v50 + 1));
                          sub_141758A00();
                          *(_BYTE *)(v53 + v52) = 0;
                          v41 = (volatile signed __int32 *)v89;
                          v48 = HIDWORD(v94);
                          v51 = v94;
                        }
                        HIDWORD(v94) = v48 + ~v50 + v38;
                        *(_BYTE *)(v51 + SHIDWORD(v94) + 8) = 0;
                      }
                    }
                  }
                }
              }
            }
            if ( _InterlockedDecrement(v41) == 0 )
              sub_1412EC9A0((__int64)v41);
            v54 = v90;
            if ( v90 != nullptr && _InterlockedDecrement(v90 - 1) == 0 )
              sub_1412EC9A0((__int64)(v54 - 1));
            v17 = false;
            v15 += 2;
            if ( v15 == v16 )
              goto LABEL_27;
          }
          v26 = v87;
          if ( v93 != 0 )
          {
            if ( HIDWORD(v94) == 0 )
              goto LABEL_43;
            v27 = v94 + 8;
            v28 = HIDWORD(v94) - 1;
            if ( *(char *)(v94 + SHIDWORD(v94) + 7) <= -65 )
              v28 = sub_1417584B0(v94 + 8, 0, v28);
            if ( (unsigned int)sub_140811DC0(v27, v28) == 10 )
            {
LABEL_43:
              v29 = *(__int64 **)(qword_141ABD468 + 8);
              v90 = nullptr;
              v30 = (__int64 *)*v29;
              v31 = (__int64 *)v30[1];
              v32 = v30;
              if ( *((_BYTE *)v31 + 25) == 0 )
              {
                v32 = v30;
                do
                {
                  v33 = v31 + 2;
                  if ( v31[4] >= (unsigned __int64)qword_141B62A20 )
                  {
                    v32 = v31;
                    v33 = v31;
                  }
                  v31 = (__int64 *)*v33;
                }
                while ( *(_BYTE *)(*v33 + 25) == 0 );
              }
              if ( *((_BYTE *)v32 + 25) == 0 && qword_141B62A20 >= (unsigned __int64)v32[4] && v32 != v30 )
              {
                v55 = v32[5];
                if ( v55 != 0 )
                {
                  v90 = (volatile signed __int32 *)v32[5];
                  _InterlockedIncrement((volatile signed __int32 *)(v55 + 8));
                }
              }
              sub_141316220(v25, &v90);
              v34 = v90;
              if ( v90 != nullptr && _InterlockedDecrement(v90 + 2) == 0 )
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v34)(v34, 1);
            }
          }
          v35 = v15 + 1;
          sub_1413142C0(v25, (unsigned int)&v90, *v15, (_DWORD)v15 + 8, *(_DWORD *)(v26 + 24) != -1);
          v17 = v91 == 0;
          if ( *(_BYTE *)(v26 + 28) == 0xFF && *v35 != 0 )
            break;
LABEL_127:
          v63 = v90;
          if ( v90 != nullptr )
          {
            v64 = (unsigned int)v91;
            if ( v91 <= 0 )
              goto LABEL_132;
            sub_140807AB0(&v94, (unsigned int)v91);
            if ( (_QWORD)v94 != 0 )
            {
              v65 = v94 + SHIDWORD(v94);
              sub_141758A00();
              *(_BYTE *)(v64 + v65 + 8) = 0;
              HIDWORD(v94) += v64;
            }
            v63 = v90;
            if ( v90 != nullptr )
            {
LABEL_132:
              if ( _InterlockedDecrement(v63) == 0 )
                sub_1412EC9A0((__int64)v63);
            }
          }
          v15 += 2;
          if ( v15 == v16 )
            goto LABEL_27;
        }
        if ( ++v88 == a3 )
        {
LABEL_55:
          *(_BYTE *)(v25 + 85) = 1;
LABEL_118:
          if ( *(_BYTE *)(v25 + 85) != 0 )
          {
            (*(void (__fastcall **)(_QWORD, __int64 *, char *))(*(_QWORD *)*v35 + 64LL))(*v35, &v86, &v92);
            if ( v92 == 0
              || (v60 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v35 + 32LL))(*v35), v61 = v60, v60 == 9999) )
            {
              v61 = (*(__int64 (__fastcall **)(_QWORD, __int64 *))(**(_QWORD **)(v25 + 40) + 32LL))(
                      *(_QWORD *)(v25 + 40),
                      &v86);
            }
            v62 = (void (__fastcall ***)(_QWORD, __int64))v86;
            if ( v86 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v86 + 8)) == 0 )
              (**v62)(v62, 1);
          }
          else
          {
            v61 = -1;
          }
          *(_BYTE *)(v87 + 28) = v61;
          goto LABEL_127;
        }
        v56 = (__int64)(*a4 + 1);
        if ( *a4 != nullptr )
        {
          v57 = **a4;
          v58 = *(_DWORD **)v25;
          if ( v57 == -1 )
          {
LABEL_115:
            v59 = (__int64)(v58 + 1);
            if ( v58 == nullptr )
              v59 = 0x1419435F1LL;
            if ( (unsigned int)sub_141758D90(v59, v56) != 0 )
              goto LABEL_118;
            goto LABEL_55;
          }
          if ( v58 == nullptr )
            goto LABEL_114;
        }
        else
        {
          v56 = 0x1419435F1LL;
          v58 = *(_DWORD **)v25;
          v57 = 0;
          if ( *(_QWORD *)v25 == 0 )
          {
LABEL_114:
            if ( v57 != 0 )
              goto LABEL_118;
            goto LABEL_115;
          }
        }
        if ( *v58 != v57 )
          goto LABEL_118;
        goto LABEL_115;
      }
      if ( v13 != nullptr && _InterlockedDecrement(v13) == 0 )
        sub_1412EC9A0((__int64)v13);
    }
    DWORD2(v94) = 0;
    _InterlockedIncrement((volatile signed __int32 *)v12);
    *(_QWORD *)&v94 = v12;
    DWORD2(v94) = *(_DWORD *)(v12 + 4);
    goto LABEL_26;
  }
}
