__int64 __fastcall sub_141F09000(_QWORD *a1, __int64 a2)
{
  void (__fastcall ***v4)(_QWORD, __int64); // rcx
  __int64 v5; // rcx
  unsigned __int16 v6; // bx
  __int64 v7; // rsi
  _DWORD *v8; // rdi
  _DWORD *v9; // rcx
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  __int64 v12; // [rsp+48h] [rbp-40h] BYREF
  __int64 v13; // [rsp+50h] [rbp-38h] BYREF
  _DWORD *v14; // [rsp+58h] [rbp-30h] BYREF
  __int64 v15; // [rsp+60h] [rbp-28h] BYREF
  __int64 v16; // [rsp+68h] [rbp-20h] BYREF

  v13 = 0;
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)*a1 + 40LL))(a1: *a1) != 0
    && (sub_1407D2400(a1: *a1, a2: &v12, a3: &unk_141AC0070), v12 != 0) )
  {
    v13 = v12;
  }
  else
  {
    sub_1407C5890(a1: &v12, a2: a1);
    if ( v12 == 0 )
      goto LABEL_14;
    sub_1407D2400(a1: v12, a2: &v15, a3: &unk_141AC0070);
    if ( v15 != 0 )
      v13 = v15;
    v4 = (void (__fastcall ***)(_QWORD, __int64))v12;
    if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 + 8)) == 0 )
      (**v4)(a1: v4, a2: 1);
    if ( v13 == 0 )
    {
LABEL_14:
      LODWORD(v7) = 0;
      return (unsigned int)v7;
    }
  }
  sub_1407D0D60(a1: &v15);
  sub_1407D0F70(
    a1: (unsigned int)&v15,
    a2: (unsigned int)&v16,
    a3: (unsigned int)&v13,
    a4: (unsigned int)&unk_141AC0078,
    a5: (__int64)&unk_141AC0080,
    a6: 0,
    a7: 0,
    0);
  v5 = v16;
  if ( v16 == 0 )
  {
    LODWORD(v7) = 0;
    goto LABEL_31;
  }
  v6 = WORD2(v15);
  if ( WORD2(v15) < 3u )
  {
    LODWORD(v7) = 0;
    goto LABEL_29;
  }
  v14 = (_DWORD *)v16;
  _InterlockedIncrement((volatile signed __int32 *)(v16 + 8));
  v8 = v14;
  sub_140814D80(a1: v14, a2: &v12, a3: a2);
  if ( (_DWORD)v12 == 0 )
  {
    sub_140814B10(a1: v8, a2: &v12, a3: a2 + 8);
    if ( (_DWORD)v12 == 0 )
    {
      sub_140814B10(a1: v8, a2: &v12, a3: a2 + 16);
      if ( (_DWORD)v12 == 0 )
      {
        sub_140814B10(a1: v8, a2: &v12, a3: a2 + 24);
        if ( (_DWORD)v12 == 0 )
        {
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a2 + 80, a3: 1);
          if ( v8[4] == 0 )
          {
            (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a2 + 81, a3: 1);
            if ( v8[4] == 0 )
            {
              (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a2 + 40, a3: 8);
              if ( v8[4] == 0 )
              {
                (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a2 + 32, a3: 8);
                if ( v8[4] == 0 )
                {
                  sub_140814B10(a1: v8, a2: &v12, a3: a2 + 48);
                  if ( (_DWORD)v12 == 0 )
                  {
                    if ( v6 < 4u )
                    {
                      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v8 + 40LL))(
                        a1: v8,
                        a2: &v12,
                        a3: 8);
                      if ( v8[4] != 0 )
                        goto LABEL_25;
                      v7 = a2 + 56;
                      sub_140242390(a1: v7, a2: 0, a3: v12);
                    }
                    else
                    {
                      v7 = a2 + 56;
                      if ( (unsigned __int8)sub_140242910(a1: v7, a2: &v14) == 0 )
                        goto LABEL_25;
                    }
                    LOBYTE(v7) = 1;
                    v9 = v14;
                    if ( v14 == nullptr )
                      goto LABEL_28;
                    goto LABEL_26;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
LABEL_25:
  LODWORD(v7) = 0;
  v9 = v14;
  if ( v14 != nullptr )
  {
LABEL_26:
    if ( _InterlockedDecrement(v9 + 2) == 0 )
      (**(void (__fastcall ***)(_DWORD *, __int64))v9)(a1: v9, a2: 1);
  }
LABEL_28:
  v5 = v16;
  if ( v16 != 0 )
  {
LABEL_29:
    if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v5)(a1: v5, a2: 1);
  }
LABEL_31:
  v10 = (void (__fastcall ***)(_QWORD, __int64))v13;
  if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    (**v10)(a1: v10, a2: 1);
  return (unsigned int)v7;
}
