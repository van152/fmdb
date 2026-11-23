// THUNK ALIAS -> sub_14455D1E0 (jmp:0x14159d690->0x14455d1e0)
__int64 __fastcall sub_14455D1E0(__int64 **a1, __int64 a2)
{
  __int64 v4; // r13
  __int64 v5; // rsi
  unsigned __int64 v6; // rbx
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 *v10; // rdi
  __int64 *v11; // rdx
  __int64 i; // rdi
  __int64 v13; // rcx
  __int64 v14; // r12
  __int64 v15; // rax
  int v16; // ecx
  char v17; // cl
  __int64 v18; // r13
  __int64 v19; // rbx
  __int64 v20; // rax
  int v21; // ecx
  char v22; // bl
  __int64 v24; // [rsp+28h] [rbp-18h] BYREF
  __int64 v25; // [rsp+30h] [rbp-10h]
  int v26; // [rsp+38h] [rbp-8h] BYREF
  int v27; // [rsp+3Ch] [rbp-4h]
  __int64 v28; // [rsp+40h] [rbp+0h]

  v28 = -2;
  v4 = **a1;
  v5 = (*a1)[1];
  v6 = (v5 - v4) >> 3;
  v7 = qword_141B60C38;
  v8 = qword_141B60C30;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    v9 = qword_141B60C30;
    while ( *(_DWORD *)v9 != 1684171881 )
    {
      v9 += 16;
      if ( v9 == qword_141B60C38 )
        goto LABEL_25;
    }
    if ( v9 != qword_141B60C38 && *(_QWORD *)(v9 + 8) != 0 )
    {
      v10 = nullptr;
      while ( *(_DWORD *)v8 != 1684171881 )
      {
        v8 += 16;
        if ( v8 == qword_141B60C38 )
          goto LABEL_15;
      }
      v10 = v8 == qword_141B60C38 ? nullptr : *(__int64 **)(v8 + 8);
LABEL_15:
      v11 = &qword_141B5A4A0;
      if ( v10 != nullptr )
        v11 = v10;
      LODWORD(i) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 64LL))(*v11);
      if ( (int)i >= 0 && v6 > (unsigned int)i )
      {
        v13 = **a1;
        v14 = *(_QWORD *)(v13 + 8LL * (unsigned int)i);
        v15 = sub_14083D4F0(v13) + 8;
        v25 = 0;
        v24 = v15;
        if ( v14 != 0 )
        {
          v16 = *(_DWORD *)(v14 + 16);
          if ( v16 == 0 )
            v16 = *(_DWORD *)(v14 + 12);
          v26 = *(_DWORD *)(v14 + 12);
          v27 = v16;
          sub_140FE72B0(&v26, 1315856756, &v24);
          v17 = sub_140DD6070(a2, &v24, 0);
          v15 = v24;
          if ( v17 != 0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, &v24);
            return (unsigned int)i;
          }
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, &v24);
      }
    }
  }
LABEL_25:
  LODWORD(i) = -1;
  if ( v5 != v4 )
  {
    v18 = 1;
    if ( v6 >= 2 )
      v18 = v6;
    for ( i = 0; i != v18; ++i )
    {
      v19 = *(_QWORD *)(**a1 + 8 * i);
      v20 = sub_14083D4F0(v7) + 8;
      v25 = 0;
      v24 = v20;
      if ( v19 != 0 )
      {
        v21 = *(_DWORD *)(v19 + 16);
        if ( v21 == 0 )
          v21 = *(_DWORD *)(v19 + 12);
        v26 = *(_DWORD *)(v19 + 12);
        v27 = v21;
        sub_140FE72B0(&v26, 1315856756, &v24);
        v22 = sub_140DD6070(a2, &v24, 0);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, &v24);
        if ( v22 != 0 )
          return (unsigned int)i;
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, &v24);
      }
    }
    LODWORD(i) = -1;
  }
  return (unsigned int)i;
}
