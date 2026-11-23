__int64 __fastcall sub_140924370(_QWORD *a1, unsigned __int8 a2, char a3)
{
  __int64 v5; // rdi
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rdi
  __int64 v10; // r14
  __int64 v11; // rbx
  __int64 v12; // rcx
  void (__fastcall ***v13)(_QWORD, __int64); // rcx
  void (__fastcall ***v14)(_QWORD, __int64); // rcx
  __int64 v15; // rdi
  __int64 v16; // rbx
  __int64 v17; // rax
  __int64 v18; // r8
  __int64 v19; // rcx
  __int64 v20; // rcx
  __int64 *v21; // rax
  __int64 *v22; // rax
  __int64 v23; // rsi
  __int64 v24; // [rsp+30h] [rbp-58h] BYREF
  unsigned __int8 v25; // [rsp+3Fh] [rbp-49h] BYREF
  __int64 v26; // [rsp+40h] [rbp-48h] BYREF
  char v27[8]; // [rsp+48h] [rbp-40h] BYREF
  __int64 v28; // [rsp+50h] [rbp-38h]
  int v29; // [rsp+60h] [rbp-28h]

  v25 = a2;
  if ( a2 == 0xFF )
    return a1[66];
  if ( (a2 & 0x80u) == 0 )
  {
    v5 = a2;
    v6 = a1[56];
    if ( (a1[57] - v6) >> 3 > (unsigned __int64)a2 )
    {
      v7 = *(_QWORD *)(v6 + 8LL * a2);
      if ( v7 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v7 + 656LL))(v7) != 6 )
      {
        v8 = *(_QWORD *)(a1[56] + 8 * v5);
        if ( v8 != 0 && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v8 + 240LL))(v8) != 0 )
          return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v8 + 240LL))(v8);
      }
    }
  }
  if ( a3 != 0 )
  {
    v10 = qword_141ABD468;
    v24 = 0;
    v11 = sub_1412EC810(264, 55);
    *(_QWORD *)v11 = 0x3700000000LL;
    strcpy((char *)(v11 + 8), "No stats found for stage index [%number#1] on [%date#1]");
    if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 - 4)) == 0 )
      sub_1412EC9A0(v24 - 4);
    v24 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v11);
    v24 = v11 + 4;
    sub_140824A20(v10, v27, &v24);
    v12 = v24;
    if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 - 4)) == 0 )
      sub_1412EC9A0(v12 - 4);
    sub_140828920(&v24, &v25);
    sub_14081D7C0(v27, 1, &v24, 0);
    v13 = (void (__fastcall ***)(_QWORD, __int64))v24;
    if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 8)) == 0 )
      (**v13)(v13, 1);
    sub_140DAB5E0(&v24, &dword_141AAE084);
    sub_14081D7C0(v27, 1, &v24, 0);
    v14 = (void (__fastcall ***)(_QWORD, __int64))v24;
    if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 8)) == 0 )
      (**v14)(v14, 1);
    v15 = qword_141ABD468;
    v26 = 0;
    if ( v29 == -1
      || (v16 = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL), *(_QWORD *)(sub_140105F10() + 16) != v16) )
    {
      sub_14081DFC0(v27, 0, 0xFFFFFFFFLL, &qword_141B59EE0);
      if ( *(_DWORD *)(*(_QWORD *)(v15 + 8) + 264LL) != 0 )
      {
        sub_14081EDF0(v27, &v24);
        v17 = v24;
        if ( v24 == 0 )
          goto LABEL_31;
      }
      else
      {
        v17 = v28;
        if ( v28 != 0 )
        {
          v26 = 0;
          _InterlockedIncrement((volatile signed __int32 *)(v28 - 4));
        }
      }
      v26 = v17;
    }
LABEL_31:
    sub_140AF88B0(&v24, a1[36], &v26);
    v19 = v26;
    if ( v26 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 - 4)) == 0 )
      sub_1412EC9A0(v19 - 4);
    v20 = v24;
    if ( v24 != 0 )
    {
      if ( *(_DWORD *)v24 == 0 )
        goto LABEL_54;
      LOBYTE(v18) = 1;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)qword_141B5AD60 + 120LL))(
             qword_141B5AD60,
             &v24,
             v18,
             0) != 0
        && (qword_141B5B710 & 0x100000000LL) != 0 )
      {
        v21 = &qword_141B5B6F8;
        while ( 1 )
        {
          v21 = (__int64 *)v21[2];
          if ( v21 == nullptr || *v21 == 0 )
            break;
          if ( (*((_BYTE *)v21 + 28) & 1) == 0 )
            goto LABEL_53;
        }
        if ( (int)qword_141B5B710 <= 1 )
        {
          v22 = &qword_141B5B6F8;
          while ( 1 )
          {
            v22 = (__int64 *)v22[2];
            if ( v22 == nullptr || *v22 == 0 )
              break;
            if ( (*((_BYTE *)v22 + 28) & 1) == 0 || *((int *)v22 + 6) > 1 )
              goto LABEL_53;
          }
          v23 = sub_1407E2C90(2160);
          sub_1407E2EB0(v23, 1099916335, 11191, 1099842527, 0, 1);
          sub_14080CDB0(v23, &v24);
          if ( (sub_1407E0380(&qword_141B5B6F8, v23) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
            __debugbreak();
        }
      }
LABEL_53:
      v20 = v24;
      if ( v24 != 0 )
      {
LABEL_54:
        if ( _InterlockedDecrement((volatile signed __int32 *)(v20 - 4)) == 0 )
          sub_1412EC9A0(v20 - 4);
      }
    }
    sub_14081D040(v27);
  }
  return 0;
}
