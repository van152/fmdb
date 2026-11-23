bool __fastcall sub_140FE5B80(_QWORD *a1, _QWORD *a2, __int64 a3, char a4)
{
  __int64 v6; // rax
  unsigned __int64 v7; // rax
  __int64 v8; // rbp
  __int64 v9; // r15
  __int64 *v10; // rdx
  _QWORD *v11; // rbx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 *v14; // r8
  unsigned int *v15; // rcx
  __int64 v16; // rbp
  volatile signed __int32 *v17; // rcx
  volatile signed __int32 *v18; // rcx
  char v19; // al
  volatile signed __int32 *v20; // rcx
  __int64 v21; // rsi
  __int64 *v22; // rdx
  __int64 v23; // rax
  __int64 v24; // rcx
  __int64 *v25; // r8
  unsigned int *v26; // rcx
  __int64 v27; // rbp
  volatile signed __int32 *v28; // rcx
  volatile signed __int32 *v29; // rcx
  char v30; // al
  volatile signed __int32 *v31; // rcx
  volatile signed __int32 *v32; // rcx
  unsigned int *v33; // rcx
  volatile signed __int32 *v35; // [rsp+30h] [rbp-68h] BYREF
  unsigned int *v36; // [rsp+38h] [rbp-60h] BYREF
  volatile signed __int32 *v37; // [rsp+40h] [rbp-58h] BYREF
  _QWORD *v38; // [rsp+48h] [rbp-50h]
  __int64 v39; // [rsp+50h] [rbp-48h]

  v38 = a1;
  sub_140835530(a1);
  v6 = a2[1] - *a2;
  if ( v6 == 0 )
    return v38[1] != *v38;
  v7 = v6 >> 3;
  v8 = 1;
  if ( v7 >= 2 )
    v8 = v7;
  v39 = v8;
  if ( a4 != 0 )
  {
    v9 = 0;
    while ( 1 )
    {
      v10 = *(__int64 **)(*a2 + 8 * v9);
      if ( v10 == nullptr )
        v10 = &qword_141B5A4A0;
      v11 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v10 + 176LL))(*v10, v10, 0);
      v12 = *v11;
      v13 = v11[1];
      v14 = nullptr;
      if ( *v11 != v13 )
      {
        while ( *(_DWORD *)v12 != 1885434984 )
        {
          v12 += 16;
          if ( v12 == v13 )
            goto LABEL_15;
        }
        if ( v12 != v13 )
        {
          v14 = *(__int64 **)(v12 + 8);
          goto LABEL_16;
        }
LABEL_15:
        v14 = nullptr;
      }
LABEL_16:
      if ( v14 == nullptr )
        v14 = &qword_141B5A4A0;
      (*(void (__fastcall **)(__int64, unsigned int **))(*(_QWORD *)*v14 + 128LL))(*v14, &v36);
      v15 = v36;
      if ( v36 != nullptr )
      {
        if ( *v36 == 0 )
          goto LABEL_33;
        v35 = nullptr;
        v16 = sub_1412EC810(264, 9);
        *(_QWORD *)v16 = 0x900000000LL;
        strcpy((char *)(v16 + 8), "graphics/");
        if ( v35 != nullptr )
        {
          v17 = v35 - 1;
          if ( _InterlockedDecrement(v35 - 1) == 0 )
            sub_1412EC9A0((__int64)v17);
        }
        v35 = nullptr;
        _InterlockedIncrement((volatile signed __int32 *)v16);
        v35 = (volatile signed __int32 *)(v16 + 4);
        sub_140809550(&v35, &v37, &v36);
        v18 = v35;
        if ( v35 != nullptr && _InterlockedDecrement(v35 - 1) == 0 )
          sub_1412EC9A0((__int64)(v18 - 1));
        v19 = sub_1407F32F0(qword_141ABE180, &v37);
        v8 = v39;
        if ( v19 != 0
          && ((unsigned int)sub_14080AB90(&v36, 0x141938EC8LL, -1, 0, 0) != -1
           || (unsigned int)sub_14080AB90(&v36, 0x141939136LL, -1, 0, 0) != -1) )
        {
          goto LABEL_63;
        }
        v20 = v37;
        if ( v37 != nullptr && _InterlockedDecrement(v37 - 1) == 0 )
          sub_1412EC9A0((__int64)(v20 - 1));
        v15 = v36;
        if ( v36 != nullptr )
        {
LABEL_33:
          if ( _InterlockedDecrement((volatile signed __int32 *)v15 - 1) == 0 )
            sub_1412EC9A0((__int64)(v15 - 1));
        }
      }
      if ( ++v9 == v8 )
        return v38[1] != *v38;
    }
  }
  v21 = 0;
  while ( 1 )
  {
    v22 = *(__int64 **)(*a2 + 8 * v21);
    if ( v22 == nullptr )
      v22 = &qword_141B5A4A0;
    v11 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v22 + 176LL))(*v22, v22, 0);
    v23 = *v11;
    v24 = v11[1];
    v25 = nullptr;
    if ( *v11 != v24 )
    {
      while ( *(_DWORD *)v23 != 1885434984 )
      {
        v23 += 16;
        if ( v23 == v24 )
          goto LABEL_45;
      }
      if ( v23 != v24 )
      {
        v25 = *(__int64 **)(v23 + 8);
        goto LABEL_46;
      }
LABEL_45:
      v25 = nullptr;
    }
LABEL_46:
    if ( v25 == nullptr )
      v25 = &qword_141B5A4A0;
    (*(void (__fastcall **)(__int64, unsigned int **))(*(_QWORD *)*v25 + 128LL))(*v25, &v36);
    v26 = v36;
    if ( v36 != nullptr )
    {
      if ( *v36 != 0 )
        break;
LABEL_61:
      if ( _InterlockedDecrement((volatile signed __int32 *)v26 - 1) == 0 )
        sub_1412EC9A0((__int64)(v26 - 1));
    }
LABEL_36:
    if ( ++v21 == v8 )
      return v38[1] != *v38;
  }
  v35 = nullptr;
  v27 = sub_1412EC810(264, 9);
  *(_QWORD *)v27 = 0x900000000LL;
  strcpy((char *)(v27 + 8), "graphics/");
  if ( v35 != nullptr )
  {
    v28 = v35 - 1;
    if ( _InterlockedDecrement(v35 - 1) == 0 )
      sub_1412EC9A0((__int64)v28);
  }
  v35 = nullptr;
  _InterlockedIncrement((volatile signed __int32 *)v27);
  v35 = (volatile signed __int32 *)(v27 + 4);
  sub_140809550(&v35, &v37, &v36);
  v29 = v35;
  if ( v35 != nullptr && _InterlockedDecrement(v35 - 1) == 0 )
    sub_1412EC9A0((__int64)(v29 - 1));
  v30 = sub_1407F32F0(qword_141ABE180, &v37);
  v8 = v39;
  if ( v30 == 0 )
  {
    v31 = v37;
    if ( v37 != nullptr && _InterlockedDecrement(v37 - 1) == 0 )
      sub_1412EC9A0((__int64)(v31 - 1));
    v26 = v36;
    if ( v36 == nullptr )
      goto LABEL_36;
    goto LABEL_61;
  }
LABEL_63:
  if ( v11 != v38 )
    sub_140836CA0(v38, *v11, (__int64)(v11[1] - *v11) >> 4);
  v32 = v37;
  if ( v37 != nullptr && _InterlockedDecrement(v37 - 1) == 0 )
    sub_1412EC9A0((__int64)(v32 - 1));
  v33 = v36;
  if ( v36 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v36 - 1) == 0 )
    sub_1412EC9A0((__int64)(v33 - 1));
  return v38[1] != *v38;
}
