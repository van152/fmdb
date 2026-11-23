__int64 __fastcall sub_143D03280(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rdx
  __int64 v4; // rcx
  __int64 *v5; // rdi
  __int64 v6; // rdi
  __int64 v7; // rcx
  __int64 v8; // rcx
  char v9; // bl
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  __int64 v12; // r14
  __int64 **v13; // rax
  __int64 *v14; // rsi
  __int64 *v15; // r12
  __int64 v16; // rdi
  unsigned int v17; // ebx
  char v18; // cl
  __int64 (__fastcall ***v19)(_QWORD, __int64); // rcx
  __int64 (__fastcall ***v20)(_QWORD, __int64); // rcx
  __int64 v21; // [rsp+40h] [rbp-58h] BYREF
  __int64 v22; // [rsp+48h] [rbp-50h] BYREF
  __int64 v23; // [rsp+50h] [rbp-48h] BYREF
  __int64 v24; // [rsp+58h] [rbp-40h] BYREF
  _BYTE v25[56]; // [rsp+60h] [rbp-38h] BYREF

  result = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v3 = *(_QWORD *)(result + 8);
  v4 = result;
  if ( *(_BYTE *)(v3 + 25) == 0 )
  {
    v4 = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v5 = (__int64 *)(v3 + 16);
      if ( *(_QWORD *)(v3 + 32) >= (unsigned __int64)qword_141B59838 )
      {
        v4 = v3;
        v5 = (__int64 *)v3;
      }
      v3 = *v5;
    }
    while ( *(_BYTE *)(*v5 + 25) == 0 );
  }
  if ( *(_BYTE *)(v4 + 25) == 0 && (unsigned __int64)qword_141B59838 >= *(_QWORD *)(v4 + 32) && v4 != result )
  {
    result = *(_QWORD *)(v4 + 40);
    v24 = result;
    if ( result != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(result + 8));
      sub_14080D0E0(a1: v25, a2: 0x1418DF862LL);
      v6 = sub_1412EC810(a1: 264, a2: 21);
      *(_QWORD *)v6 = 0x1500000000LL;
      strcpy((char *)(v6 + 8), "starting_club_debt_db");
      _InterlockedIncrement((volatile signed __int32 *)v6);
      v23 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v6);
      v23 = v6 + 4;
      v22 = 0x80100004E554C4CLL;
      result = sub_1407D0F70(
                 a1: (unsigned int)&v22,
                 a2: (unsigned int)&v21,
                 a3: (unsigned int)&v24,
                 a4: (unsigned int)&v23,
                 a5: (__int64)v25,
                 a6: 0,
                 a7: 0,
                 0);
      v7 = v23;
      if ( v23 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 - 4)) == 0 )
        result = sub_1412EC9A0(a1: v7 - 4);
      if ( _InterlockedDecrement((volatile signed __int32 *)v6) == 0 )
        result = sub_1412EC9A0(a1: v6);
      if ( v21 != 0 )
      {
        sub_140F265D0(a1: a1[110]);
        v8 = a1[110];
        v22 = v21;
        if ( v21 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v21 + 8));
        v9 = sub_140F33190(a1: v8, a2: &v22, a3: a1);
        v10 = (void (__fastcall ***)(_QWORD, __int64))v22;
        if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
          (**v10)(a1: v10, a2: 1);
        if ( v9 != 0 )
        {
          v11 = (void (__fastcall ***)(_QWORD, __int64))v21;
          if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 8)) == 0 )
            (**v11)(a1: v11, a2: 1);
          v21 = 0;
          v12 = a1[110];
          v13 = *(__int64 ***)(v12 + 128);
          v14 = *v13;
          v15 = v13[1];
          while ( v14 != v15 )
          {
            v16 = *v14;
            if ( *v14 != 0 )
            {
              v17 = *(unsigned __int8 *)(v12 + 90);
              sub_140F804A0(a1, a2: v16 + 24, a3: *(unsigned __int8 *)(v12 + 90), a4: 0);
              sub_140F7F010(a1, a2: v16 + 32, a3: v17, a4: 0);
            }
            ++v14;
          }
          result = *(_BYTE *)(a1[12] + 89LL) | 2u;
          if ( *(_BYTE *)(*a1 + 89LL) == 0 )
            result = *(unsigned __int8 *)(a1[12] + 89LL);
          v18 = result | 4;
          if ( *(_BYTE *)(a1[13] + 89LL) == 0 )
            v18 = result;
          *(_BYTE *)(v12 + 90) = v18;
        }
        else
        {
          result = sub_140F265D0(a1: a1[110]);
        }
        v19 = (__int64 (__fastcall ***)(_QWORD, __int64))v21;
        if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 8)) == 0 )
          result = (**v19)(a1: v19, a2: 1);
      }
      v20 = (__int64 (__fastcall ***)(_QWORD, __int64))v24;
      if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 8)) == 0 )
        return (**v20)(a1: v20, a2: 1);
    }
  }
  return result;
}
