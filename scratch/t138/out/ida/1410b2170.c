_QWORD *__fastcall sub_1410B2170(__int64 a1, _QWORD *a2, int *a3)
{
  __int64 v6; // rbp
  __int64 v7; // rcx
  __int64 v8; // rcx
  unsigned int v9; // ebp
  __int64 *v10; // rax
  __int64 v11; // rdi
  __int64 v12; // rcx
  unsigned __int64 v13; // rbx
  __int64 v14; // rax
  __int64 v15; // rcx
  int v16; // eax
  __int64 *v17; // rax
  __int64 v18; // rcx
  __int64 v19; // rbx
  bool v20; // bp
  __int64 v21; // rdi
  __int64 v22; // rdx
  __int64 v23; // rcx
  __int64 *v24; // rax
  __int64 v25; // rax
  _QWORD *v26; // rbx
  __int64 v27; // rbx
  __int64 v28; // r8
  __int64 v29; // rax
  char v30; // bl
  void (__fastcall ***v31)(_QWORD, __int64); // rcx
  _QWORD *v32; // rbx
  _DWORD *v33; // rbp
  __int64 v34; // rdi
  __int64 v35; // rbx
  __int64 v37; // rdi
  unsigned int v38; // eax
  __int64 v39; // rbx
  __int64 v40; // r8
  __int64 v41; // rax
  char v42; // bl
  void (__fastcall ***v43)(_QWORD, __int64); // rcx
  _DWORD *v44; // rbp
  __int64 v45; // rbp
  __int64 v46; // rdi
  __int64 v47; // rdi
  __int64 v48; // rdx
  __int64 v49; // [rsp+40h] [rbp-88h] BYREF
  unsigned int v50; // [rsp+4Ch] [rbp-7Ch] BYREF
  __int128 v51; // [rsp+50h] [rbp-78h] BYREF
  __int64 v52; // [rsp+60h] [rbp-68h]
  __int64 v53; // [rsp+70h] [rbp-58h] BYREF
  _QWORD *v54; // [rsp+78h] [rbp-50h] BYREF
  _QWORD v55[9]; // [rsp+80h] [rbp-48h] BYREF

  if ( byte_141B595A8 != 0 )
  {
    v6 = qword_141B595B0;
    if ( v6 == (unsigned int)MEMORY[0x141947498]() )
      goto LABEL_3;
LABEL_13:
    if ( (qword_141B61FF0 & 0x100000000LL) == 0 || (int)qword_141B61FF0 > 1 )
      goto LABEL_98;
    v10 = &qword_141B61FD8;
    while ( 1 )
    {
      v10 = (__int64 *)v10[2];
      if ( v10 == nullptr || *v10 == 0 )
        break;
      if ( (*((_BYTE *)v10 + 28) & 1) == 0 || *((int *)v10 + 6) > 1 )
        goto LABEL_98;
    }
    v11 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v11, a2: 1099980086, a3: 769, a4: 1099809750, a5: 0, a6: 1);
    v12 = *(_QWORD *)(v11 + 2128);
    v13 = v12 - 2017;
    if ( (unsigned __int64)(v12 - 2017) >= 0x20 )
    {
      v14 = v11 + v12 + 80;
      *(_QWORD *)(v11 + 2128) = v12 + 32;
    }
    else
    {
      v14 = sub_141750CC0(a1: 32);
    }
    *(_QWORD *)(v14 + 8) = 0;
    *(_QWORD *)v14 = 0x14185CC48LL;
    *(_QWORD *)(v14 + 24) = 0x14191DA80LL;
    *(_BYTE *)(v14 + 16) = v13 >= 0x20;
    if ( *(_QWORD *)(v11 + 2136) == 0 )
      *(_QWORD *)(v11 + 2136) = v14;
    v15 = *(_QWORD *)(v11 + 2144);
    if ( v15 != 0 )
      *(_QWORD *)(v15 + 8) = v14;
    *(_QWORD *)(v11 + 2144) = v14;
    *(_QWORD *)(v11 + 24) = &qword_141B61FD8;
    v16 = HIDWORD(qword_141B61FF0) | *(_DWORD *)(v11 + 20);
    *(_DWORD *)(v11 + 20) = v16;
    if ( (v16 & 0x2000) != 0 )
      sub_1407E30A0(a1: v11);
    if ( (sub_1407E1A60(a1: v11) & 4) == 0 )
      goto LABEL_98;
    goto LABEL_31;
  }
  if ( qword_141B5A658 != (unsigned int)MEMORY[0x141947498]() )
    goto LABEL_13;
LABEL_3:
  if ( *a3 == -1 )
    goto LABEL_98;
  v7 = *(_QWORD *)(a1 + 80);
  if ( v7 == 0 )
  {
    LOWORD(v49) = 0;
    sub_141210320(a1, a2: &v51, a3: &v49);
    v8 = *(_QWORD *)(a1 + 80);
    if ( v8 == (_QWORD)v51 )
    {
      if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v8)(a1: v8, a2: 1);
    }
    else
    {
      if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v8)(a1: v8, a2: 1);
      *(_QWORD *)(a1 + 80) = v51;
    }
    v9 = (unsigned __int16)v49;
    if ( (unsigned __int16)v49 >= *(_WORD *)(a1 + 160) )
    {
      if ( (unsigned __int16)v49 > *(_WORD *)(a1 + 160) )
      {
        if ( (qword_141B61FF0 & 0x100000000LL) == 0 || (int)qword_141B61FF0 > 1 )
          goto LABEL_98;
        v17 = &qword_141B61FD8;
        while ( 1 )
        {
          v17 = (__int64 *)v17[2];
          if ( v17 == nullptr || *v17 == 0 )
            break;
          if ( (*((_BYTE *)v17 + 28) & 1) == 0 || *((int *)v17 + 6) > 1 )
            goto LABEL_98;
        }
        v35 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v35, a2: 1099980086, a3: 796, a4: 1099809750, a5: 0, a6: 1);
        sub_1407E0010(a1: v35, a2: 0x14194017ELL);
        sub_1407DFB20(a1: v35, a2: v9);
        sub_1407E0010(a1: v35, a2: 0x141941AD4LL);
        sub_1407DFB20(a1: v35, a2: *(unsigned __int16 *)(a1 + 160));
        goto LABEL_96;
      }
    }
    else
    {
      *(_WORD *)(a1 + 160) = v49;
      *(_DWORD *)(a1 + 156) = 20;
    }
    v7 = *(_QWORD *)(a1 + 80);
    if ( v7 != 0 )
      goto LABEL_43;
    if ( (qword_141B61FF0 & 0x100000000LL) == 0 || (int)qword_141B61FF0 > 1 )
      goto LABEL_98;
    v24 = &qword_141B61FD8;
    while ( 1 )
    {
      v24 = (__int64 *)v24[2];
      if ( v24 == nullptr || *v24 == 0 )
        break;
      if ( (*((_BYTE *)v24 + 28) & 1) == 0 || *((int *)v24 + 6) > 1 )
        goto LABEL_98;
    }
    v35 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v35, a2: 1099980086, a3: 804, a4: 1099809750, a5: 0, a6: 1);
    sub_1407E0010(a1: v35, a2: 0x141941629LL);
LABEL_96:
    sub_14080CDB0(a1: v35, a2: a1 + 16);
    sub_14080CDB0(a1: v35, a2: *(_QWORD *)(a1 + 32));
    v22 = v35;
LABEL_97:
    if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v22) & 4) == 0 )
      goto LABEL_98;
LABEL_31:
    if ( (unsigned int)MEMORY[0x1419475E0]() != 0 )
      __debugbreak();
    goto LABEL_98;
  }
LABEL_43:
  if ( *(_DWORD *)(a1 + 152) == 0 )
    *(_DWORD *)(a1 + 152) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 8LL))(a1: v7);
  v18 = *(_QWORD *)(a1 + 64);
  if ( v18 == 0 )
  {
    *(_QWORD *)&v51 = 0x80100004E554C4CLL;
    sub_1407D0F70(a1: (unsigned int)&v51, a2: (unsigned int)&v49, a3: a1, a4: a1 + 8, a5: a1 + 32, a6: 1, a7: 0, 0);
    v23 = *(_QWORD *)(a1 + 64);
    if ( v23 == v49 )
    {
      if ( v23 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v23)(a1: v23, a2: 1);
      v18 = *(_QWORD *)(a1 + 64);
      if ( v18 == 0 )
        goto LABEL_98;
    }
    else
    {
      if ( v23 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v23)(a1: v23, a2: 1);
      v18 = v49;
      *(_QWORD *)(a1 + 64) = v49;
      if ( v18 == 0 )
        goto LABEL_98;
    }
  }
  (*(void (__fastcall **)(__int64, __int128 *, __int64))(*(_QWORD *)v18 + 24LL))(a1: v18, a2: &v51, a3: 8LL * *a3);
  if ( (_DWORD)v51 != 0 )
    goto LABEL_98;
  v49 = -1;
  v19 = *(_QWORD *)(a1 + 64);
  if ( v19 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v19 + 8));
  (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v19 + 40LL))(a1: v19, a2: &v49, a3: 4);
  if ( *(_DWORD *)(v19 + 16) == 0 )
  {
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v19 + 40LL))(a1: v19, a2: (char *)&v49 + 4, a3: 4);
    v20 = *(_DWORD *)(v19 + 16) == 0;
    if ( _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) != 0 )
      goto LABEL_52;
    goto LABEL_51;
  }
  v20 = false;
  if ( _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
LABEL_51:
    (**(void (__fastcall ***)(__int64, __int64))v19)(a1: v19, a2: 1);
LABEL_52:
  if ( !v20 || HIDWORD(v49) == -1 )
    goto LABEL_98;
  (*(void (__fastcall **)(_QWORD, __int128 *, _QWORD))(**(_QWORD **)(a1 + 80) + 24LL))(
    a1: *(_QWORD *)(a1 + 80),
    a2: &v51,
    a3: (int)v49);
  if ( (_DWORD)v51 == 0 )
  {
    v25 = sub_1407E4940();
    v26 = (_QWORD *)sub_1407E4490(a1: v25, a2: 24);
    if ( qword_141ABD470 == 0 )
      qword_141ABD470 = sub_1407E4940();
    v26[2] = 0;
    v26[1] = 0;
    *v26 = 0;
    v54 = v26;
    v27 = sub_140F6BA00(a1: 64);
    sub_141454310(a1: v27);
    v53 = v27;
    v28 = *(unsigned __int16 *)(a1 + 160);
    v29 = *(_QWORD *)(a1 + 80);
    *(_QWORD *)&v51 = v29;
    if ( v29 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v29 + 8));
    v30 = sub_1414550A0(a1: v27, a2: &v51, a3: v28);
    v31 = (void (__fastcall ***)(_QWORD, __int64))v51;
    if ( (_QWORD)v51 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v51 + 8)) == 0 )
      (**v31)(a1: v31, a2: 1);
    if ( v30 != 0 )
    {
      v32 = v54;
      sub_1410B86E0(a1: v54);
      sub_14087F540(a1: v32, a2: &v53);
      v33 = *(_DWORD **)(a1 + 80);
      (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)v33 + 40LL))(a1: v33, a2: &v50, a3: 4);
      if ( v33[4] == 0 )
      {
        sub_141210100(a1, a2: &v50, a3: *(unsigned int *)(a1 + 152));
        if ( qword_141ABE200 == 0 )
          qword_141ABE200 = sub_1407E6540();
        v51 = 0;
        v52 = 0;
        sub_1410B8840(a1: &v51);
        if ( (_DWORD)v49 == HIDWORD(v49) || (v38 = v50, v50 == -1) )
        {
LABEL_123:
          v54 = nullptr;
        }
        else
        {
          while ( 1 )
          {
            (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD))(**(_QWORD **)(a1 + 80) + 24LL))(
              a1: *(_QWORD *)(a1 + 80),
              a2: v55,
              a3: (int)v38);
            if ( LODWORD(v55[0]) != 0 )
            {
              if ( (unsigned __int8)sub_1410B8800() == 0 )
                goto LABEL_140;
              v46 = sub_1407E2C90(a1: 2160);
              sub_1407E2EB0(a1: v46, a2: 1099980086, a3: 895, a4: 1099809750, a5: 0, a6: 1);
              goto LABEL_134;
            }
            v39 = sub_140F6BA00(a1: 64);
            sub_141454310(a1: v39);
            v53 = v39;
            v40 = *(unsigned __int16 *)(a1 + 160);
            v41 = *(_QWORD *)(a1 + 80);
            v55[0] = v41;
            if ( v41 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v41 + 8));
            v42 = sub_1414550A0(a1: v39, a2: v55, a3: v40);
            v43 = (void (__fastcall ***)(_QWORD, __int64))v55[0];
            if ( v55[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v55[0] + 8LL)) == 0 )
              (**v43)(a1: v43, a2: 1);
            if ( v42 == 0 )
              break;
            v32 = v54;
            sub_14087F540(a1: v54, a2: &v53);
            if ( v50 == HIDWORD(v49) )
              goto LABEL_123;
            v44 = *(_DWORD **)(a1 + 80);
            (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)v44 + 40LL))(
              a1: v44,
              a2: &v50,
              a3: 4);
            if ( v44[4] != 0 )
            {
              if ( (unsigned __int8)sub_1410B8800() == 0 )
                goto LABEL_140;
              v46 = sub_1407E2C90(a1: 2160);
              sub_1407E2EB0(a1: v46, a2: 1099980086, a3: 918, a4: 1099809750, a5: 0, a6: 1);
LABEL_134:
              v48 = 0x1418E103BLL;
LABEL_137:
              sub_1407E0010(a1: v46, a2: v48);
              if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v46) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
                __debugbreak();
              goto LABEL_140;
            }
            v45 = *((_QWORD *)&v51 + 1);
            if ( sub_141751AC0(a1: v51, a2: *((_QWORD *)&v51 + 1), a3: v50) != v45 )
            {
              if ( (unsigned __int8)sub_1410B8800() == 0 )
                goto LABEL_140;
              v46 = sub_1407E2C90(a1: 2160);
              sub_1407E2EB0(a1: v46, a2: 1099980086, a3: 924, a4: 1099809750, a5: 0, a6: 1);
              v48 = 0x1418DC93ALL;
              goto LABEL_137;
            }
            sub_141210100(a1, a2: &v50, a3: *(unsigned int *)(a1 + 152));
            sub_1410B8910(a1: &v51, a2: &v50);
            v38 = v50;
            if ( v50 == -1 )
              goto LABEL_123;
          }
          if ( (unsigned __int8)sub_1410B8800() != 0 )
          {
            v47 = sub_1407E2C90(a1: 2160);
            sub_1407E2EB0(a1: v47, a2: 1099980086, a3: 903, a4: 1099809750, a5: 0, a6: 1);
            sub_1407E0010(a1: v47, a2: 0x1418E103BLL);
            if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v47) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
              __debugbreak();
          }
          if ( v53 != 0 )
          {
            sub_140F6BAB0();
            v32 = nullptr;
            goto LABEL_141;
          }
LABEL_140:
          v32 = nullptr;
        }
LABEL_141:
        *a2 = v32;
        if ( (_QWORD)v51 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: v51, a3: v52 - v51);
        goto LABEL_107;
      }
      if ( (unsigned __int8)sub_1410B8800() != 0 )
      {
        v34 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v34, a2: 1099980086, a3: 876, a4: 1099809750, a5: 0, a6: 1);
        sub_1407E0010(a1: v34, a2: 0x1418E103BLL);
        if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v34) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
          __debugbreak();
      }
    }
    else
    {
      if ( (unsigned __int8)sub_1410B8800() != 0 )
      {
        v37 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v37, a2: 1099980086, a3: 862, a4: 1099809750, a5: 0, a6: 1);
        sub_1407E0010(a1: v37, a2: 0x1418E103BLL);
        if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v37) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
          __debugbreak();
      }
      if ( v53 != 0 )
        sub_140F6BAB0();
    }
    *a2 = 0;
LABEL_107:
    sub_1410B1EF0(a1: &v54);
    return a2;
  }
  if ( (unsigned __int8)sub_1410B8800() != 0 )
  {
    v21 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v21, a2: 1099980086, a3: 851, a4: 1099809750, a5: 0, a6: 1);
    sub_1407E0010(a1: v21, a2: 0x1418E103BLL);
    v22 = v21;
    goto LABEL_97;
  }
LABEL_98:
  *a2 = 0;
  return a2;
}
