__int64 __fastcall sub_143949810(_QWORD *a1, unsigned int a2)
{
  unsigned int v4; // edi
  __int64 *v6; // rdi
  __int64 *v7; // rsi
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rsi
  __int64 v11; // rdi
  __int64 v12; // r8
  __int64 v13; // rcx
  __int64 *v14; // r14
  double v15; // xmm6_8
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rdx
  __int64 *v19; // rdx
  unsigned int v20; // eax
  __int64 v21; // rcx
  __int64 v22; // [rsp+28h] [rbp-40h] BYREF

  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 1
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 2
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 15
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 24
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 26
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 0
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 25
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 5 )
  {
    return (*(unsigned int (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 64LL))(*a1, a1);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a1 + 8LL))(*a1, a1) == 10 )
  {
    v6 = nullptr;
    v7 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a1 + 176LL))(*a1, a1, 0);
    v8 = *v7;
    v9 = v7[1];
    if ( *v7 != v9 )
    {
      v6 = nullptr;
      while ( *(_DWORD *)v8 != 1667330920 )
      {
        v8 += 16;
        if ( v8 == v9 )
          goto LABEL_26;
      }
      if ( v8 == v9 )
        v6 = nullptr;
      else
        v6 = *(__int64 **)(v8 + 8);
    }
LABEL_26:
    v14 = &qword_141B5A4A0;
    if ( v6 == nullptr )
      v6 = &qword_141B5A4A0;
    v15 = (*(double (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v6 + 112LL))(*v6, v6);
    v16 = *v7;
    v17 = v7[1];
    if ( *v7 != v17 )
    {
      v18 = *v7;
      while ( *(_DWORD *)v18 != 1668641394 )
      {
        v18 += 16;
        if ( v18 == v17 )
          return (unsigned int)(int)v15;
      }
      if ( v18 != v17 && *(_QWORD *)(v18 + 8) != 0 )
      {
        v19 = nullptr;
        while ( *(_DWORD *)v16 != 1668641394 )
        {
          v16 += 16;
          if ( v16 == v17 )
            goto LABEL_42;
        }
        if ( v16 == v17 )
          v19 = nullptr;
        else
          v19 = *(__int64 **)(v16 + 8);
LABEL_42:
        if ( v19 != nullptr )
          v14 = v19;
        v20 = sub_140A3D250(v14, a2);
        v15 = sub_140DA5D60(v21, v20, 0, 0);
      }
    }
    return (unsigned int)(int)v15;
  }
  else
  {
    v10 = qword_141B5AD60;
    v22 = 0;
    v11 = sub_1412EC810(264, 35);
    *(_QWORD *)v11 = 0x2300000000LL;
    strcpy((char *)(v11 + 8), "cash is neither a integer or record");
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 - 4)) == 0 )
      sub_1412EC9A0(v22 - 4);
    v22 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v11);
    v22 = v11 + 4;
    v4 = 0;
    LOBYTE(v12) = 1;
    (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v10 + 120LL))(v10, &v22, v12, 0);
    v13 = v22;
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 - 4)) == 0 )
      sub_1412EC9A0(v13 - 4);
  }
  return v4;
}
