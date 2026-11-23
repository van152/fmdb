__int64 __fastcall sub_140E52DE0(__int64 a1, int a2, __int128 *a3)
{
  __int128 *v3; // rbx
  int v6; // ecx
  int v7; // ecx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 *v10; // rax
  __int64 v11; // rax
  bool v12; // zf
  __int64 v13; // rax
  __int64 v14; // rdx
  __int64 v15; // rdx
  __int64 v16; // rdi
  __int64 v17; // rax
  __int64 v18; // rdi
  unsigned int v19; // eax
  unsigned int v20; // ecx
  __int64 v21; // rdx
  __int64 v22; // rax
  __int64 *v23; // r13
  __int64 *v24; // r12
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 *v27; // r13
  __int64 *v28; // r12
  __int64 v29; // rax
  __int64 v30; // rcx
  int v31; // eax
  __int64 *v32; // r15
  _QWORD *v33; // rdi
  __int64 v34; // rcx
  __int64 v35; // rdx
  __int64 *v36; // rax
  __int64 *v37; // r15
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 *v40; // rdx
  __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 *v43; // rax
  _QWORD *v44; // rax
  __int64 v45; // rdi
  _QWORD v47[2]; // [rsp+20h] [rbp-50h] BYREF
  _QWORD v48[2]; // [rsp+30h] [rbp-40h] BYREF
  _QWORD v49[2]; // [rsp+40h] [rbp-30h] BYREF
  __int128 v50; // [rsp+50h] [rbp-20h] BYREF
  __int64 v51; // [rsp+60h] [rbp-10h]
  __int64 v52; // [rsp+70h] [rbp+0h]

  v52 = -2;
  v3 = a3;
  (*(void (__fastcall **)(_QWORD, __int128 *, _QWORD *))(**(_QWORD **)a3 + 24LL))(*(_QWORD *)a3, a3, v49);
  if ( a2 <= 1347183217 )
  {
    if ( a2 > 1346786155 )
    {
      if ( a2 <= 1346795360 )
      {
        if ( a2 <= 1346790515 )
        {
          if ( a2 == 1346786156 || a2 == 1346790252 || a2 == 1346790259 )
            goto LABEL_109;
        }
        else if ( a2 > 1346792046 )
        {
          if ( a2 == 1346792047 || a2 == 1346794598 )
            goto LABEL_109;
        }
        else if ( a2 == 1346790516 || a2 == 1346790756 )
        {
          goto LABEL_109;
        }
        goto LABEL_202;
      }
      if ( a2 > 1347174722 )
      {
        if ( (unsigned int)(a2 - 1347174723) <= 0x11 )
        {
          v6 = 196609;
          if ( _bittest(&v6, a2 - 1347174723) )
            goto LABEL_109;
        }
        if ( a2 == 1347176044 || a2 == 1347178055 )
          goto LABEL_109;
        goto LABEL_202;
      }
      if ( a2 == 1346795361 || a2 == 1346795376 )
        goto LABEL_109;
      if ( a2 != 1346916944 )
        goto LABEL_202;
    }
    else
    {
      if ( a2 <= 1315140192 )
      {
        if ( a2 <= 1112567145 )
        {
          if ( a2 == 1098081136 )
          {
            if ( *(_BYTE *)(a1 + 101) == 18 )
            {
              v31 = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(*(_QWORD *)v3, v3);
              switch ( v31 )
              {
                case 1:
                  *(_WORD *)(a1 + 80) = 4250;
                  break;
                case 2:
                  *(_WORD *)(a1 + 80) = 6250;
                  break;
                case 3:
                  *(_WORD *)(a1 + 80) = 7750;
                  break;
                default:
                  *(_WORD *)(a1 + 80) = 2125;
                  break;
              }
            }
            goto LABEL_202;
          }
          if ( a2 != 1112490825 )
          {
            if ( a2 != 1112566383 )
              goto LABEL_202;
LABEL_112:
            v16 = qword_141B5FE40;
            sub_140FE7960(&v50, v3, 1416914273);
            v17 = sub_140FA3700(v16, &v50);
            if ( v17 != 0 )
            {
              v18 = v17;
              v19 = *(_DWORD *)(v17 + 12);
              v20 = *(_DWORD *)(v18 + 16);
              if ( v20 == 0 )
                v20 = v19;
              *(_QWORD *)&v50 = __PAIR64__(v20, v19);
              sub_140FE72B0(&v50, 1416914273, v49);
              *(_QWORD *)(a1 + 32) = v18;
              *(_BYTE *)(a1 + 102) &= ~8u;
              if ( *(_QWORD *)(a1 + 48) == 0 )
              {
                v21 = 368;
                if ( *(_BYTE *)(v18 + 47) == 0 )
                  v21 = 216;
                *(_QWORD *)(a1 + 48) = *(_QWORD *)(*(_QWORD *)(v18 + 48) + v21);
              }
            }
            else
            {
              *(_QWORD *)&v50 = -1;
              sub_140FE72B0(&v50, 1416914273, v49);
              if ( *(_QWORD *)(a1 + 32) != 0 )
                *(_BYTE *)(a1 + 102) |= 8u;
            }
            LOBYTE(v3) = 1;
            if ( a2 != 1112566383 && (byte_141B5D974 & 1) == 0 )
              goto LABEL_203;
            goto LABEL_207;
          }
          *(_DWORD *)(a1 + 64) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(
                                   *(_QWORD *)v3,
                                   v3);
        }
        else
        {
          if ( a2 > 1129271384 )
          {
            if ( a2 == 1129271385 )
            {
              sub_141084920(a1, 1129271385, v3);
              if ( v49 != (_QWORD *)v3 )
              {
                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v49[0] + 16LL))(v49[0], v49);
                (*(void (__fastcall **)(_QWORD, __int128 *, _QWORD *))(**(_QWORD **)v3 + 24LL))(*(_QWORD *)v3, v3, v49);
              }
            }
            else if ( a2 == 1145392197
                   && ((unsigned __int8)sub_140087040() == 0
                    || (_DWORD)(v15 = *(unsigned int *)(a1 + 12)) == -1
                    || sub_1400568B0(qword_141B5FE10) == 0) )
            {
              *(_BYTE *)(a1 + 103) = 0;
              LOBYTE(v15) = 8;
              sub_140E53AE0(a1, v15, 0);
            }
            goto LABEL_202;
          }
          if ( a2 == 1112567146 )
          {
            *(_WORD *)(a1 + 94) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 80LL))(
                                    *(_QWORD *)v3,
                                    v3);
          }
          else
          {
            if ( a2 != 1112756292 )
              goto LABEL_202;
            byte_141B5D974 = 1;
            v8 = (*(__int64 (__fastcall **)(_QWORD, __int128 *, _QWORD))(**(_QWORD **)v3 + 176LL))(*(_QWORD *)v3, v3, 0);
            sub_1407EAF60(a1, v8);
            byte_141B5D974 = 0;
          }
        }
LABEL_206:
        LOBYTE(v3) = 1;
        goto LABEL_207;
      }
      if ( a2 > 1316450929 )
      {
        if ( a2 > 1346587214 )
        {
          if ( a2 == 1346587215 )
          {
            *(_WORD *)(a1 + 94) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 80LL))(
                                    *(_QWORD *)v3,
                                    v3);
            goto LABEL_202;
          }
          if ( a2 != 1346589264 )
            goto LABEL_202;
          goto LABEL_124;
        }
        if ( a2 == 1316450930 )
          goto LABEL_126;
        if ( a2 != 1346584898 )
          goto LABEL_202;
LABEL_64:
        *(_WORD *)(a1 + 86) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(
                                *(_QWORD *)v3,
                                v3);
        goto LABEL_202;
      }
      if ( a2 <= 1315466609 )
      {
        if ( a2 != 1315140193 )
        {
          if ( a2 != 1315140210 )
            goto LABEL_202;
LABEL_124:
          *(_WORD *)(a1 + 82) = 50
                              * (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(
                                  *(_QWORD *)v3,
                                  v3);
          goto LABEL_202;
        }
        goto LABEL_64;
      }
      if ( a2 != 1315466610 )
      {
        if ( a2 != 1315992673 )
          goto LABEL_202;
        goto LABEL_85;
      }
    }
    *(_WORD *)(a1 + 84) = 50
                        * (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(*(_QWORD *)v3, v3);
    goto LABEL_202;
  }
  if ( a2 <= 1347187565 )
  {
    if ( a2 <= 1347184235 )
    {
      if ( a2 > 1347183971 )
      {
        if ( a2 == 1347183972 || a2 == 1347184226 )
          goto LABEL_109;
      }
      else
      {
        if ( (unsigned int)(a2 - 1347183468) <= 8 )
        {
          v7 = 323;
          if ( _bittest(&v7, a2 - 1347183468) )
            goto LABEL_109;
        }
        if ( a2 == 1347183218 )
          goto LABEL_109;
      }
    }
    else if ( a2 > 1347186529 )
    {
      if ( (unsigned int)(a2 - 1347186530) < 2 || a2 == 1347186759 || a2 == 1347187556 )
        goto LABEL_109;
    }
    else if ( a2 > 1347186018 )
    {
      if ( a2 == 1347186019 || a2 == 1347186022 )
        goto LABEL_109;
    }
    else if ( a2 == 1347184236 || a2 == 1347184995 )
    {
      goto LABEL_109;
    }
    goto LABEL_202;
  }
  if ( a2 <= 1348759393 )
  {
    if ( a2 <= 1347449683 )
    {
      if ( a2 <= 1347308110 )
      {
        if ( a2 != 1347187566 && a2 != 1347188579 )
          goto LABEL_202;
LABEL_109:
        LODWORD(v3) = sub_141084920(a1, (unsigned int)a2, v3);
        goto LABEL_207;
      }
      if ( a2 == 1347308111 )
      {
        *(_WORD *)(a1 + 98) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 80LL))(
                                *(_QWORD *)v3,
                                v3);
        goto LABEL_202;
      }
      if ( a2 != 1347436866 )
        goto LABEL_202;
LABEL_85:
      *(_WORD *)(a1 + 88) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(*(_QWORD *)v3, v3);
      goto LABEL_202;
    }
    if ( a2 <= 1347899983 )
    {
      if ( a2 == 1347449684 )
        goto LABEL_109;
      if ( a2 == 1347635791 )
        *(_WORD *)(a1 + 96) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 80LL))(
                                *(_QWORD *)v3,
                                v3);
      goto LABEL_202;
    }
    if ( a2 != 1347899984 )
    {
      if ( a2 != 1348695145 )
        goto LABEL_202;
      goto LABEL_112;
    }
LABEL_126:
    *(_WORD *)(a1 + 80) = 50
                        * (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(*(_QWORD *)v3, v3);
    goto LABEL_202;
  }
  if ( a2 > 1349411177 )
  {
    if ( a2 > 1349804393 )
    {
      if ( a2 != 1349804394 )
      {
        if ( a2 == 1349810544 )
          *(_BYTE *)(a1 + 101) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 64LL))(
                                   *(_QWORD *)v3,
                                   v3);
        goto LABEL_202;
      }
      v27 = nullptr;
      v28 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, __int128 *, _QWORD))(**(_QWORD **)v3 + 176LL))(
                         *(_QWORD *)v3,
                         v3,
                         0);
      v29 = *v28;
      v30 = v28[1];
      if ( *v28 != v30 )
      {
        v27 = nullptr;
        while ( *(_DWORD *)v29 != 1416914273 )
        {
          v29 += 16;
          if ( v29 == v30 )
            goto LABEL_174;
        }
        if ( v29 == v30 )
          v27 = nullptr;
        else
          v27 = *(__int64 **)(v29 + 8);
      }
LABEL_174:
      v37 = &qword_141B5A4A0;
      if ( v27 == nullptr )
        v27 = &qword_141B5A4A0;
      v33 = (_QWORD *)(a1 + 32);
      sub_140FE7E20(a1 + 32, v27);
      if ( *(_QWORD *)(a1 + 32) != 0 )
      {
        v38 = *v28;
        v39 = v28[1];
        v40 = nullptr;
        if ( *v28 != v39 )
        {
          while ( *(_DWORD *)v38 != 1349151845 )
          {
            v38 += 16;
            if ( v38 == v39 )
              goto LABEL_189;
          }
          if ( v38 == v39 )
            v40 = nullptr;
          else
            v40 = *(__int64 **)(v38 + 8);
        }
LABEL_189:
        if ( v40 == nullptr )
          v40 = &qword_141B5A4A0;
        *(_WORD *)(a1 + 94) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v40 + 80LL))(*v40);
        v41 = *v28;
        v42 = v28[1];
        v43 = nullptr;
        if ( *v28 != v42 )
        {
          while ( *(_DWORD *)v41 != 1349741167 )
          {
            v41 += 16;
            if ( v41 == v42 )
              goto LABEL_198;
          }
          if ( v41 == v42 )
            v43 = nullptr;
          else
            v43 = *(__int64 **)(v41 + 8);
        }
LABEL_198:
        if ( v43 != nullptr )
          v37 = v43;
        *(_WORD *)(a1 + 96) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v37 + 80LL))(*v37, v37);
      }
    }
    else
    {
      if ( a2 != 1349411178 )
      {
        if ( a2 == 1349416041 )
          sub_140FE7D20(a1 + 48, v3);
        goto LABEL_202;
      }
      v23 = nullptr;
      v24 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, __int128 *, _QWORD))(**(_QWORD **)v3 + 176LL))(
                         *(_QWORD *)v3,
                         v3,
                         0);
      v25 = *v24;
      v26 = v24[1];
      if ( *v24 != v26 )
      {
        v23 = nullptr;
        while ( *(_DWORD *)v25 != 1416914273 )
        {
          v25 += 16;
          if ( v25 == v26 )
            goto LABEL_164;
        }
        if ( v25 == v26 )
          v23 = nullptr;
        else
          v23 = *(__int64 **)(v25 + 8);
      }
LABEL_164:
      v32 = &qword_141B5A4A0;
      if ( v23 == nullptr )
        v23 = &qword_141B5A4A0;
      v33 = (_QWORD *)(a1 + 40);
      sub_140FE7E20(a1 + 40, v23);
      if ( *(_QWORD *)(a1 + 40) != 0 )
      {
        v34 = *v24;
        v35 = v24[1];
        v36 = nullptr;
        if ( *v24 != v35 )
        {
          while ( *(_DWORD *)v34 != 1349151845 )
          {
            v34 += 16;
            if ( v34 == v35 )
              goto LABEL_184;
          }
          if ( v34 == v35 )
            v36 = nullptr;
          else
            v36 = *(__int64 **)(v34 + 8);
        }
LABEL_184:
        if ( v36 != nullptr )
          v32 = v36;
        *(_WORD *)(a1 + 98) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v32 + 80LL))(*v32, v32);
      }
    }
    v48[1] = 0;
    v48[0] = sub_14083D4F0() + 8;
    v44 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, __int128 *, _QWORD))(**(_QWORD **)v3 + 176LL))(
                      *(_QWORD *)v3,
                      v3,
                      0);
    v50 = 0;
    v51 = 0;
    v3 = &v50;
    sub_1408367A0(&v50, (__int64)(v44[1] - *v44) >> 4, v44, v44 + 1);
    sub_140FCC150(*v33, v48);
    sub_1408351C0(&v50, 1416914273, v48);
    sub_14083DC80(v47, &v50);
    sub_14083DFA0(v49, v47);
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v47[0] + 16LL))(v47[0], v47);
    sub_140833970(&v50);
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v48[0] + 16LL))(v48[0], v48);
    goto LABEL_202;
  }
  if ( a2 > 1349083503 )
  {
    if ( a2 == 1349083504 )
    {
      *(_BYTE *)(a1 + 100) = (*(__int64 (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)v3 + 80LL))(*(_QWORD *)v3, v3);
    }
    else if ( a2 == 1349411177 )
    {
      *(_QWORD *)&v50 = 0;
      sub_140FE7D20(&v50, v3);
      if ( (_QWORD)v50 == 0 )
        goto LABEL_155;
      if ( (*(_BYTE *)(a1 + 25) & 0x10) == 0 || (v9 = *(_QWORD *)(v50 + 272)) == 0 )
        v9 = *(_QWORD *)(v50 + 264);
      v10 = *(__int64 **)(v9 + 24);
      if ( v10 == *(__int64 **)(v9 + 32) )
      {
LABEL_155:
        *(_QWORD *)(a1 + 40) = 0;
      }
      else
      {
        v11 = *v10;
        *(_QWORD *)(a1 + 40) = v11;
        if ( v11 != 0 && *(_QWORD *)(a1 + 48) == 0 )
        {
          v12 = *(_BYTE *)(v11 + 47) == 0;
          v13 = *(_QWORD *)(v11 + 48);
          v14 = 368;
          if ( v12 )
            v14 = 216;
          *(_QWORD *)(a1 + 48) = *(_QWORD *)(v13 + v14);
        }
      }
    }
  }
  else
  {
    if ( a2 == 1348759394 )
    {
      v22 = sub_140DBC940();
      sub_140DBCA60(v22, &v50, v3);
      *(_WORD *)(a1 + 90) = WORD1(v50);
      goto LABEL_202;
    }
    if ( a2 == 1348887138 )
      goto LABEL_109;
  }
LABEL_202:
  LOBYTE(v3) = 1;
  if ( byte_141B5D974 == 0 )
  {
LABEL_203:
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v49[0] + 8LL))(v49[0], v49) == 10 )
    {
      v45 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)v49[0] + 176LL))(v49[0], v49, 0);
      sub_141109FB0(v45);
      v3 = &v50;
      sub_14083DC80(&v50, v45);
      sub_140F4AAF0(&qword_141B5FDA8, (unsigned int)a2, &v50);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v50 + 16LL))(v50, &v50);
    }
    else
    {
      sub_140F4AAF0(&qword_141B5FDA8, (unsigned int)a2, v49);
    }
    goto LABEL_206;
  }
LABEL_207:
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v49[0] + 16LL))(v49[0], v49);
  return (unsigned int)v3;
}
