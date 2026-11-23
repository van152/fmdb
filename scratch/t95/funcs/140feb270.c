__int64 __fastcall sub_140FEB270(_DWORD *a1, _QWORD *a2)
{
  __int64 *v3; // rdi
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rdx
  _QWORD *v9; // rbx
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 *v12; // rax
  __int64 *v13; // rdi
  __int64 *v14; // rsi
  int v15; // eax
  _DWORD *v16; // r14
  unsigned __int64 i; // rdx
  char v18; // bl
  bool v19; // bl
  __int64 v20; // rcx
  __int64 v21; // rdx
  __int64 *v22; // rax
  __int64 *v23; // rdi
  __int64 *v24; // rsi
  int *v25; // rcx
  int *v26; // [rsp+20h] [rbp-20h] BYREF
  _QWORD v27[7]; // [rsp+28h] [rbp-18h] BYREF

  v27[2] = -2;
  v3 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a2 + 176LL))(*a2, a2, 0);
  v5 = sub_14083D4F0(v4) + 8;
  v27[1] = 0;
  v27[0] = v5;
  v6 = *v3;
  v7 = v3[1];
  if ( *v3 == v7 )
    goto LABEL_4;
  while ( *(_DWORD *)v6 != 1685218662 )
  {
    v6 += 16;
    if ( v6 == v7 )
      goto LABEL_4;
  }
  if ( v6 == v7 || (v9 = *(_QWORD **)(v6 + 8)) == nullptr )
  {
LABEL_4:
    *a1 = -8388609;
    return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
  }
  if ( v9 != v27 )
  {
    (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v5 + 16LL))(v5, v27);
    (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*v9 + 24LL))(*v9, v9, v27);
    v5 = v27[0];
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v5 + 8LL))(v5, v27) == 1
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 2
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 15
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 24
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 25
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 5 )
  {
    *a1 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 64LL))(v27[0], v27);
    v10 = *v3;
    v11 = v3[1];
    v12 = nullptr;
    if ( *v3 != v11 )
    {
      while ( *(_DWORD *)v10 != 1684237940 )
      {
        v10 += 16;
        if ( v10 == v11 )
          goto LABEL_23;
      }
      if ( v10 == v11 )
        v12 = nullptr;
      else
        v12 = *(__int64 **)(v10 + 8);
    }
LABEL_23:
    v13 = &qword_141B5A4A0;
    if ( v12 != nullptr )
      v13 = v12;
    v14 = (__int64 *)(a1 + 2);
    if ( v14 != v13 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v14 + 16LL))(*v14, v14);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v13 + 24LL))(*v13, v13, v14);
    }
    return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
  }
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) != 26 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 8LL))(v27[0], v27) == 10 )
    {
      sub_140FEB270(a1, v27);
      return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
    }
    goto LABEL_4;
  }
  (*(void (__fastcall **)(_QWORD, int **, _QWORD *))(*(_QWORD *)v27[0] + 128LL))(v27[0], &v26, v27);
  if ( v26 != nullptr )
  {
    v15 = *v26;
    v16 = v26 + 1;
    if ( *v26 == -1 )
      v15 = sub_141758DB0(v16);
    if ( v15 > 0 )
    {
      for ( i = 0; i < (unsigned int)v15; ++i )
      {
        v18 = *((_BYTE *)v16 + i);
        if ( v18 == 45 )
          v19 = v15 != 1 && i == 0;
        else
          v19 = (unsigned __int8)(v18 - 48) < 0xAu;
        if ( !v19 )
          break;
      }
      if ( v19 )
      {
        *a1 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)v27[0] + 64LL))(
                v27[0],
                v27,
                (unsigned int)v15);
        v20 = *v3;
        v21 = v3[1];
        v22 = nullptr;
        if ( *v3 != v21 )
        {
          while ( *(_DWORD *)v20 != 1684237940 )
          {
            v20 += 16;
            if ( v20 == v21 )
              goto LABEL_48;
          }
          if ( v20 == v21 )
            v22 = nullptr;
          else
            v22 = *(__int64 **)(v20 + 8);
        }
LABEL_48:
        v23 = &qword_141B5A4A0;
        if ( v22 != nullptr )
          v23 = v22;
        v24 = (__int64 *)(a1 + 2);
        if ( v24 != v23 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v24 + 16LL))(*v24, v24);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v23 + 24LL))(*v23, v23, v24);
        }
      }
    }
    v25 = v26;
    if ( v26 != nullptr && _InterlockedDecrement(v26 - 1) == 0 )
      sub_1412EC9A0((__int64)(v25 - 1));
  }
  return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
}
