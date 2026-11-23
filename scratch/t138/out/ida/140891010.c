__int64 __fastcall sub_140891010(__int64 a1, int a2, __int64 *a3)
{
  volatile signed __int32 **v4; // r14
  __int64 v5; // rdi
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 v8; // rcx
  __int64 v9; // rax
  _DWORD *v10; // rcx
  __int64 v11; // rcx
  _DWORD *v12; // rbx
  __int64 v13; // rdi
  __int64 v14; // rcx
  __int64 *v17; // rax
  __int64 *v18; // rdx
  __int64 *v19; // rcx
  __int64 *v20; // rsi
  void (__fastcall ***v21)(_QWORD, __int64); // rcx
  __int64 v22; // rdi
  __int64 v23; // rdx
  __int64 v24; // rcx
  __int64 v25; // r15
  bool v26; // al
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 v29; // rax
  volatile signed __int32 *v30; // rcx
  void (__fastcall ***v31)(_QWORD, __int64); // rcx
  void (__fastcall ***v32)(_QWORD, __int64); // rcx
  __int64 v33; // [rsp+40h] [rbp-68h] BYREF
  __int64 v34; // [rsp+48h] [rbp-60h] BYREF
  __int64 v35; // [rsp+50h] [rbp-58h] BYREF
  int v36; // [rsp+5Ch] [rbp-4Ch] BYREF
  __int64 v37; // [rsp+60h] [rbp-48h] BYREF
  _BYTE v38[64]; // [rsp+68h] [rbp-40h] BYREF

  v36 = a2;
  v4 = (volatile signed __int32 **)(a1 + 208);
  if ( *(_QWORD *)(a1 + 208) == 0 )
  {
    v34 = 0;
    v17 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    v18 = (__int64 *)v17[1];
    v19 = v17;
    if ( *((_BYTE *)v18 + 25) == 0 )
    {
      v19 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
      do
      {
        v20 = v18 + 2;
        if ( v18[4] >= (unsigned __int64)qword_141B5ACC0 )
        {
          v19 = v18;
          v20 = v18;
        }
        v18 = (__int64 *)*v20;
      }
      while ( *(_BYTE *)(*v20 + 25) == 0 );
    }
    if ( *((_BYTE *)v19 + 25) != 0 || qword_141B5ACC0 < (unsigned __int64)v19[4] || v19 == v17 )
    {
      v33 = 0;
    }
    else
    {
      v27 = v19[5];
      v33 = v27;
      if ( v27 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v27 + 8));
    }
    sub_1407C3450(a1: &v35, a2: &v33, a3: &v34);
    v21 = (void (__fastcall ***)(_QWORD, __int64))v33;
    if ( v33 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 + 8)) == 0 )
      (**v21)(a1: v21, a2: 1);
    v22 = v34;
    if ( v34 != 0 && _InterlockedDecrement((volatile signed __int32 *)v34) == 0 )
    {
      sub_1408B5D70(a1: *(_QWORD *)(*(_QWORD *)(v22 + 8) + 8LL));
      v23 = *(_QWORD *)(v22 + 8);
      if ( v23 != 0 )
      {
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v24 = *(_QWORD *)(qword_141ABD470 + 24),
              (unsigned __int64)(*(_QWORD *)(qword_141ABD470 + 32) - v24) >= 0x181)
          && (v25 = *(_QWORD *)(v24 + 384)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v25 + 32, a2: v23 - *(unsigned int *)(v25 + 120));
          v26 = *(_BYTE *)(v25 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) != 0;
          if ( !v26 && *(_BYTE *)(v25 + 97) != 0 )
            sub_1412D33C0(a1: v25);
        }
        else
        {
          MEMORY[0x141948990](a1: v23 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      sub_141750CFC(a1: v22);
    }
    if ( v35 != 0 )
    {
      sub_14080D0E0(a1: v38, a2: 0x14191EB1BLL);
      v34 = 0x80100004E554C4CLL;
      sub_1407D0F70(
        a1: (unsigned int)&v34,
        a2: (unsigned int)&v33,
        a3: (unsigned int)&v35,
        a4: (unsigned int)&qword_141B5ACC8,
        a5: (__int64)v38,
        a6: 4,
        a7: 0,
        a8: 0);
      v28 = *(_QWORD *)(a1 + 200);
      if ( v28 == v33 )
      {
        if ( v28 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v28)(a1: v28, a2: 1);
        v29 = *(_QWORD *)(a1 + 200);
        if ( v29 == 0 )
          goto LABEL_78;
      }
      else
      {
        if ( v28 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v28)(a1: v28, a2: 1);
        v29 = v33;
        *(_QWORD *)(a1 + 200) = v33;
        if ( v29 == 0 )
          goto LABEL_78;
      }
      v33 = v29;
      _InterlockedIncrement((volatile signed __int32 *)(v29 + 8));
      sub_1407C5A20(a1: &v34, a2: &v33, a3: &v35, a4: &qword_141B5ACC8);
      v30 = *v4;
      if ( *v4 == (volatile signed __int32 *)v34 )
      {
        if ( v30 != nullptr && _InterlockedDecrement(v30 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v30)(a1: v30, a2: 1);
      }
      else
      {
        if ( v30 != nullptr && _InterlockedDecrement(v30 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v30)(a1: v30, a2: 1);
        *v4 = (volatile signed __int32 *)v34;
        v34 = 0;
      }
      v31 = (void (__fastcall ***)(_QWORD, __int64))v33;
      if ( v33 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 + 8)) == 0 )
        (**v31)(a1: v31, a2: 1);
LABEL_78:
      v32 = (void (__fastcall ***)(_QWORD, __int64))v35;
      if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 + 8)) == 0 )
        (**v32)(a1: v32, a2: 1);
    }
  }
  sub_1408085A0(a1: &v34, a2: &v36);
  v33 = 0;
  v5 = sub_1412EC810(a1: 264, a2: 9);
  *(_QWORD *)v5 = 0x900000000LL;
  strcpy((char *)(v5 + 8), "fixtures_");
  if ( v33 != 0 )
  {
    v6 = v33 - 4;
    if ( _InterlockedDecrement((volatile signed __int32 *)(v33 - 4)) == 0 )
      sub_1412EC9A0(a1: v6);
  }
  v33 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v33 = v5 + 4;
  sub_140809550(a1: &v33, a2: &v35, a3: &v34);
  v7 = v33;
  if ( v33 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  v8 = v34;
  if ( v34 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 - 4)) == 0 )
    sub_1412EC9A0(a1: v8 - 4);
  sub_14080D0E0(a1: v38, a2: 0x14191EB1BLL);
  v37 = 0;
  v9 = v35;
  if ( v35 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v35 - 4));
  v37 = v9;
  v34 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v34,
    a2: (unsigned int)&v33,
    a3: (_DWORD)v4,
    a4: (unsigned int)&v37,
    a5: (__int64)v38,
    a6: 4,
    a7: 0,
    a8: 0);
  v10 = (_DWORD *)*a3;
  if ( *a3 == v33 )
  {
    if ( v10 != nullptr && _InterlockedDecrement(v10 + 2) == 0 )
      (**(void (__fastcall ***)(_DWORD *, __int64))v10)(a1: v10, a2: 1);
  }
  else
  {
    if ( v10 != nullptr && _InterlockedDecrement(v10 + 2) == 0 )
      (**(void (__fastcall ***)(_DWORD *, __int64))v10)(a1: v10, a2: 1);
    *a3 = v33;
    v33 = 0;
  }
  v11 = v37;
  if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 - 4)) == 0 )
    sub_1412EC9A0(a1: v11 - 4);
  v12 = (_DWORD *)*a3;
  if ( *a3 == 0 )
    goto LABEL_27;
  (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v12 + 40LL))(a1: *a3, a2: &v33, a3: 1);
  LODWORD(v13) = 0;
  if ( v12[4] == 0 && (_BYTE)v33 == 9 )
  {
    v13 = *a3;
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v34, a3: 4);
    if ( *(_DWORD *)(v13 + 16) == 0 && (_DWORD)v34 == v36 )
    {
      LOBYTE(v13) = *a3 != 0;
      goto LABEL_28;
    }
LABEL_27:
    LODWORD(v13) = 0;
  }
LABEL_28:
  v14 = v35;
  if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 - 4)) == 0 )
    sub_1412EC9A0(a1: v14 - 4);
  return (unsigned int)v13;
}
