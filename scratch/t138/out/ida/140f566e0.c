__int64 __fastcall sub_140F566E0(__int64 a1, int a2, char a3, _WORD *a4, void (__fastcall *a5)(_QWORD), __int64 a6)
{
  __int64 v10; // rsi
  char v11; // bp
  __int64 v12; // rdi
  __int64 v13; // rcx
  __int64 v14; // rax
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  void (__fastcall ***v16)(_QWORD, __int64); // rcx
  __int64 v17; // rdx
  char v18; // bl
  __int64 v19; // r9
  void (__fastcall ***v20)(_QWORD, __int64); // rcx
  int v21; // edi
  void (__fastcall ***v22)(_QWORD, __int64); // rcx
  void (__fastcall ***v23)(_QWORD, __int64); // rcx
  char v24; // al
  __int64 v25; // rax
  _QWORD *v26; // rdi
  _QWORD *v27; // rbx
  char v28; // al
  char v29; // cl
  void (__fastcall ***v30)(_QWORD, __int64); // rcx
  void (__fastcall ***v31)(_QWORD, __int64); // rcx
  void (__fastcall ***v32)(_QWORD, __int64); // rcx
  __int16 v33; // cx
  int v35; // [rsp+20h] [rbp-88h]
  __int64 v36; // [rsp+48h] [rbp-60h] BYREF
  __int64 v37; // [rsp+50h] [rbp-58h] BYREF
  __int64 v38; // [rsp+58h] [rbp-50h] BYREF
  __int64 v39; // [rsp+60h] [rbp-48h] BYREF
  __int64 v40; // [rsp+68h] [rbp-40h] BYREF

  v10 = a6;
  if ( a6 == 0 )
    v10 = *(_QWORD *)(a1 + 104);
  sub_140F237E0(a1: v10);
  if ( (*(_BYTE *)(v10 + 92) & 2) != 0 )
  {
    *(_BYTE *)(v10 + 89) = 1;
    LOBYTE(v10) = 1;
  }
  else
  {
    if ( a3 != 0 )
      goto LABEL_57;
    v11 = *(_BYTE *)(v10 + 90);
    v40 = 0x80100004E554C4CLL;
    sub_14080D0E0(a1: &v38, a2: 0x1418E2C24LL);
    v12 = sub_1412EC810(a1: 264, a2: 15);
    *(_QWORD *)v12 = 0xF00000000LL;
    strcpy((char *)(v12 + 8), "basic_people_db");
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v36 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v36 = v12 + 4;
    sub_1407D0F70(
      a1: (unsigned int)&v40,
      a2: (unsigned int)&v39,
      a3: a2,
      a4: (unsigned int)&v36,
      a5: (__int64)&v38,
      a6: 0,
      a7: 0,
      0);
    v13 = v36;
    if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
      sub_1412EC9A0(a1: v13 - 4);
    if ( _InterlockedDecrement((volatile signed __int32 *)v12) == 0 )
      sub_1412EC9A0(a1: v12);
    v14 = v39;
    if ( v39 != 0 )
    {
      *(_WORD *)(a1 + 1416) = WORD2(v40);
      v36 = v14;
      _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
      sub_1407CC0B0(a1: &v38, a2: &v36);
      v15 = (void (__fastcall ***)(_QWORD, __int64))v36;
      if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
        (**v15)(a1: v15, a2: 1);
      v37 = v38;
      if ( v38 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v38 + 8));
      sub_140803850(a1: &v36, a2: &v37, a3: 0x10000);
      v16 = (void (__fastcall ***)(_QWORD, __int64))v37;
      if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 + 8)) == 0 )
        (**v16)(a1: v16, a2: 1);
      *(_BYTE *)(a1 + 1451) = 1;
      v37 = v36;
      if ( v36 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v36 + 8));
      v18 = sub_140F2FE70(a1: v10, a2: &v37, a3: a1);
      v20 = (void (__fastcall ***)(_QWORD, __int64))v37;
      if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 + 8)) == 0 )
        (**v20)(a1: v20, a2: 1);
      v21 = 1;
      if ( v18 != 0 )
      {
        *(_BYTE *)(a1 + 1451) = 0;
        v22 = (void (__fastcall ***)(_QWORD, __int64))v36;
        if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
          (**v22)(a1: v22, a2: 1);
        v36 = 0;
        v23 = (void (__fastcall ***)(_QWORD, __int64))v38;
        if ( v38 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 8)) == 0 )
          (**v23)(a1: v23, a2: 1);
        v38 = 0;
        v24 = (v11 | *(_BYTE *)(v10 + 90)) & 0xFB;
        if ( v11 != 32 )
          v24 = v11 | *(_BYTE *)(v10 + 90);
        *(_BYTE *)(v10 + 90) = v24;
        v25 = *(_QWORD *)(v10 + 128);
        v26 = *(_QWORD **)v25;
        v27 = *(_QWORD **)(v25 + 8);
        while ( v26 != v27 )
        {
          if ( *v26 != 0 )
          {
            LOBYTE(v35) = *(_BYTE *)(v10 + 90);
            LOBYTE(v17) = 1;
            LOBYTE(v19) = 1;
            (*(void (__fastcall **)(_QWORD, __int64, __int64, __int64, int))(*(_QWORD *)*v26 + 160LL))(
              a1: *v26,
              a2: v17,
              a3: a1,
              a4: v19,
              a5: v35);
          }
          ++v26;
        }
        v28 = *(_BYTE *)(*(_QWORD *)(a1 + 96) + 89LL) | 2;
        if ( *(_BYTE *)(*(_QWORD *)a1 + 89LL) == 0 )
          v28 = *(_BYTE *)(*(_QWORD *)(a1 + 96) + 89LL);
        v29 = v28 | 4;
        if ( *(_BYTE *)(*(_QWORD *)(a1 + 104) + 89LL) == 0 )
          v29 = v28;
        *(_BYTE *)(v10 + 90) = v29;
        v21 = 0;
        if ( v10 == *(_QWORD *)(a1 + 104) )
          *(_DWORD *)(a1 + 1480) = (*(_QWORD *)(*(_QWORD *)(v10 + 128) + 8LL) - **(_QWORD **)(v10 + 128)) >> 3;
      }
      v30 = (void (__fastcall ***)(_QWORD, __int64))v36;
      if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
        (**v30)(a1: v30, a2: 1);
      v31 = (void (__fastcall ***)(_QWORD, __int64))v38;
      if ( v38 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 8)) == 0 )
        (**v31)(a1: v31, a2: 1);
    }
    else
    {
      sub_140F2B090();
      v21 = 1;
    }
    v32 = (void (__fastcall ***)(_QWORD, __int64))v39;
    if ( v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 + 8)) == 0 )
      (**v32)(a1: v32, a2: 1);
    if ( v21 == 0 )
    {
LABEL_57:
      LOBYTE(v10) = 1;
      if ( a4 != nullptr )
      {
        v33 = *a4 + 1;
        *a4 = v33;
        if ( a5 != nullptr )
          a5(a1: (unsigned int)v33);
      }
    }
    else
    {
      LODWORD(v10) = 0;
    }
  }
  return (unsigned int)v10;
}
