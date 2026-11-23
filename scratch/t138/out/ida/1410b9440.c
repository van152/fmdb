__int64 __fastcall sub_1410B9440(__int64 a1, _QWORD *a2)
{
  char *v4; // rdi
  __int64 v6; // rax
  __int64 v7; // r8
  __int64 v8; // r8
  __int16 v9; // r14
  __int16 v10; // cx
  __int64 v11; // rax
  __int64 v12; // rax
  void (__fastcall ***v13)(_QWORD, __int64); // rcx
  _DWORD v14[2]; // [rsp+24h] [rbp-3Ch] BYREF
  int v15; // [rsp+2Ch] [rbp-34h] BYREF
  _DWORD *v16; // [rsp+30h] [rbp-30h] BYREF
  int *v17; // [rsp+38h] [rbp-28h]
  __int64 v18; // [rsp+40h] [rbp-20h]
  char *v19; // [rsp+48h] [rbp-18h]
  __int16 v20; // [rsp+54h] [rbp-Ch] BYREF
  char v21; // [rsp+56h] [rbp-Ah] BYREF
  char v22; // [rsp+57h] [rbp-9h] BYREF
  _QWORD v23[5]; // [rsp+58h] [rbp-8h] BYREF

  v23[0] = -2;
  sub_140814B10(a1: *a2, a2: &v16, a3: a1);
  if ( (_DWORD)v16 != 0 )
  {
    LODWORD(v4) = 0;
  }
  else
  {
    v6 = *a2;
    v16 = (_DWORD *)v6;
    if ( v6 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v6 + 8));
    v18 = 0;
    v19 = nullptr;
    v17 = v14;
    if ( &v15 == (int *)&v20 )
    {
      v18 = 10;
      v7 = 14;
    }
    else
    {
      if ( v16 != nullptr )
        (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v14, a3: 8);
      v17 = (int *)&v20;
      v18 = 2;
      v7 = 6;
    }
    v19 = &v21;
    if ( &v21 == (char *)&v15 )
    {
      v18 = v7;
    }
    else
    {
      if ( v16 != nullptr )
        (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17);
      v19 = nullptr;
      v17 = &v15;
      v18 = 4;
      v7 = 4;
    }
    if ( &v16 == (_DWORD **)&v22 )
    {
      v18 = v7 + 1;
      v8 = v7 + 2;
    }
    else
    {
      if ( v16 != nullptr )
        (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17, a3: v7);
      v17 = (int *)&v22;
      v18 = 1;
      v8 = 2;
    }
    v19 = (char *)v23;
    v4 = &v21;
    if ( v23 != (_QWORD *)&v21 )
    {
      if ( v18 != 0 && v16 != nullptr )
        (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17);
      v18 = 0;
      v17 = (int *)&v21;
      v8 = 1;
    }
    v18 = v8;
    v19 = &v22;
    sub_1412E70A0(a1: &v16);
    if ( v18 != 0 && v16 != nullptr )
      (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17);
    v19 = nullptr;
    v18 = 0;
    v17 = nullptr;
    LOBYTE(v4) = v16[4] == 0;
    if ( v16[4] == 0 )
    {
      *(_DWORD *)(a1 + 8) = v14[0];
      *(_WORD *)(a1 + 14) = v20;
      *(_BYTE *)(a1 + 19) = v21;
      *(_BYTE *)(a1 + 18) = v22;
      v9 = -1;
      v10 = -1;
      if ( v14[1] >= 0 )
      {
        v11 = sub_1400568B0(a1: qword_141B5FDD0);
        v10 = -1;
        if ( v11 != 0 )
          v10 = *(_WORD *)(v11 + 8);
      }
      *(_WORD *)(a1 + 12) = v10;
      if ( v15 >= 0 )
      {
        v12 = sub_140F74E40(a1: qword_141B5FE00);
        if ( v12 != 0 )
          v9 = *(_WORD *)(v12 + 8);
      }
      *(_WORD *)(a1 + 16) = v9;
    }
    if ( v18 != 0 )
    {
      if ( v16 == nullptr )
        return (unsigned int)v4;
      (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17);
    }
    v13 = (void (__fastcall ***)(_QWORD, __int64))v16;
    v19 = nullptr;
    v18 = 0;
    v17 = nullptr;
    if ( v16 != nullptr && _InterlockedDecrement(v16 + 2) == 0 )
      (**v13)(a1: v13, a2: 1);
  }
  return (unsigned int)v4;
}
