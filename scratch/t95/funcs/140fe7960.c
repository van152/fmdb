__int64 __fastcall sub_140FE7960(__int64 a1, __int64 *a2, unsigned int a3)
{
  char v6; // al
  __int64 v7; // rcx
  __int64 v8; // rbx
  char v9; // al
  __int64 *v10; // rax
  __int64 v11; // rcx
  __int64 *v12; // rsi
  __int64 v13; // rbx
  __int64 v14; // r13
  __int64 v15; // rsi
  unsigned __int64 v16; // rsi
  __int64 **v17; // r12
  __int64 v18; // rcx
  char v19; // al
  char v20; // al
  __int64 v21; // rsi
  int v22; // eax
  __int64 v23; // rax
  __int64 v24; // rax
  char v25; // al
  __int64 v26; // rbx
  __int64 v28; // rax
  __int64 v29; // rax
  int v30; // ecx
  int v31; // eax
  __int64 v32; // rsi
  int v33; // eax
  __int64 v34; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v35[10]; // [rsp+30h] [rbp-10h] BYREF

  v35[2] = -2;
  while ( 1 )
  {
LABEL_2:
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 8LL))(*a2, a2) == 0 )
      goto LABEL_38;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 8LL))(*a2, a2) == 10 )
      break;
    v6 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 8LL))(*a2, a2);
    v7 = *a2;
    v8 = *(_QWORD *)*a2;
    if ( v6 == 15 )
    {
LABEL_21:
      v23 = (*(__int64 (__fastcall **)(__int64, __int64 *))(v8 + 64))(v7, a2);
LABEL_39:
      *(_QWORD *)a1 = v23;
      return a1;
    }
    v9 = (*(__int64 (__fastcall **)(__int64, __int64 *))(v8 + 8))(v7, a2);
    a3 = 0;
    if ( v9 != 10 )
    {
LABEL_19:
      v21 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 64LL))(*a2, a2);
      v22 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 64LL))(*a2, a2);
      if ( v21 == v22 )
      {
        *(_DWORD *)a1 = v22;
        *(_DWORD *)(a1 + 4) = 0;
      }
      else
      {
        *(_QWORD *)a1 = v21;
      }
      return a1;
    }
  }
  v10 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*a2 + 176LL))(*a2, a2, 0);
  v12 = v10;
  if ( a3 != 0 )
  {
    v35[0] = 0;
    v34 = sub_14083D4F0(v11) + 8;
    if ( (unsigned __int8)sub_1408358E0(v12, a3, &v34) != 0 )
    {
      v25 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 8LL))(v34, &v34);
      v26 = *(_QWORD *)v34;
      if ( v25 == 15 )
      {
        *(_QWORD *)a1 = (*(__int64 (__fastcall **)(__int64, __int64 *))(v26 + 64))(v34, &v34);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(v26 + 8))(v34, &v34) == 10 )
      {
        sub_140FE7960(a1, &v34, 0);
      }
      else
      {
        v32 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 64LL))(v34, &v34);
        v33 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 64LL))(v34, &v34);
        if ( v32 == v33 )
        {
          *(_DWORD *)a1 = v33;
          *(_DWORD *)(a1 + 4) = 0;
        }
        else
        {
          *(_QWORD *)a1 = v32;
        }
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 16LL))(v34, &v34);
    }
    else
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 16LL))(v34, &v34);
      v13 = *v12;
      v14 = v12[1];
LABEL_35:
      if ( v13 == v14 )
        goto LABEL_38;
      while ( *(_DWORD *)v13 != 1685218662 )
      {
        v13 += 16;
        if ( v13 == v14 )
          goto LABEL_38;
      }
      if ( v13 == v14 || *(_QWORD *)(v13 + 8) == 0 )
      {
LABEL_38:
        v23 = qword_141B60BE0;
        goto LABEL_39;
      }
      v28 = sub_14083D4F0(v18);
      v35[1] = 0;
      v35[0] = v28 + 8;
      sub_140FEB270(&v34, a2);
      v29 = sub_140F8F320(&v34);
      *(_DWORD *)a1 = -1;
      if ( v29 != 0 )
      {
        v30 = *(_DWORD *)(v29 + 12);
        *(_DWORD *)a1 = v30;
        v31 = *(_DWORD *)(v29 + 16);
        if ( v31 == 0 )
          v31 = v30;
      }
      else
      {
        v31 = -1;
      }
      *(_DWORD *)(a1 + 4) = v31;
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v35[0] + 16LL))(v35[0], v35);
    }
  }
  else
  {
    v13 = *v10;
    v14 = v10[1];
    v15 = v14 - *v10;
    if ( v15 != 0 )
    {
      v16 = v15 >> 4;
      if ( v16 < 2 )
        v16 = 1;
      v17 = (__int64 **)(v13 + 8);
      do
      {
        if ( (unsigned __int8)sub_140A434E0(*((unsigned int *)v17 - 2)) != 0 )
        {
          a2 = *v17;
          if ( *v17 == nullptr )
            a2 = &qword_141B5A4A0;
          v19 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 8LL))(*a2, a2);
          v7 = *a2;
          v8 = *(_QWORD *)*a2;
          if ( v19 == 15 )
            goto LABEL_21;
          v20 = (*(__int64 (__fastcall **)(__int64, __int64 *))(v8 + 8))(v7, a2);
          a3 = 0;
          if ( v20 == 10 )
            goto LABEL_2;
          goto LABEL_19;
        }
        v17 += 2;
        --v16;
      }
      while ( v16 != 0 );
      if ( v13 != v14 )
      {
        v24 = v13;
        while ( *(_DWORD *)v24 != 1685218662 )
        {
          v24 += 16;
          if ( v24 == v14 )
            goto LABEL_30;
        }
        if ( v24 != v14 && *(_QWORD *)(v24 + 8) != 0 )
          goto LABEL_35;
      }
    }
LABEL_30:
    *(_QWORD *)a1 = -1;
  }
  return a1;
}
