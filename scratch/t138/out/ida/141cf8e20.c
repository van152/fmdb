__int64 __fastcall sub_141CF8E20(__int64 a1)
{
  __int64 result; // rax
  volatile signed __int32 *v3; // rcx
  volatile signed __int32 *v4; // rsi
  __int64 v5; // rdi
  __int64 v7; // rax
  __int64 v8; // rax
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rsi
  volatile signed __int32 *v11; // rcx
  volatile signed __int32 *v12; // [rsp+30h] [rbp-98h] BYREF
  volatile signed __int32 *v13; // [rsp+38h] [rbp-90h] BYREF
  volatile signed __int32 *v14; // [rsp+40h] [rbp-88h] BYREF
  _QWORD v15[3]; // [rsp+48h] [rbp-80h] BYREF
  char v16[8]; // [rsp+60h] [rbp-68h] BYREF
  _BYTE v17[24]; // [rsp+68h] [rbp-60h] BYREF
  _BYTE v18[72]; // [rsp+80h] [rbp-48h] BYREF

  result = sub_1407D5DC0(a1: qword_141ABD878, a2: &v12, a3: &qword_141B597F0);
  if ( v12 == nullptr )
    return result;
  result = (*(__int64 (__fastcall **)(volatile signed __int32 *, _QWORD *, void *, __int64 *))(*(_QWORD *)v12 + 208LL))(
             a1: v12,
             a2: v15,
             a3: &unk_141ABD900,
             a4: &qword_141B59858);
  v3 = v12;
  if ( v12 != (volatile signed __int32 *)v15[0] )
  {
    if ( v12 != nullptr && _InterlockedDecrement(v12 + 2) == 0 )
      result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v3)(a1: v3, a2: 1);
    v4 = (volatile signed __int32 *)v15[0];
    v12 = (volatile signed __int32 *)v15[0];
    if ( v15[0] == 0 )
      return result;
LABEL_12:
    v13 = nullptr;
    sub_1407D8AB0(a1: v15, a2: 0x1418E2C24LL);
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, _BYTE *, __int64 *, _QWORD *, volatile signed __int32 **, int))(*(_QWORD *)v4 + 216LL))(
               a1: v4,
               a2: v17,
               a3: &qword_141B59758,
               a4: v15,
               a5: &v13,
               a6: 1);
    if ( v13 != nullptr )
    {
      result = sub_1407D4670();
      if ( result != 0 )
      {
        v5 = result - 1;
        do
        {
          sub_1407D46A0(a1: v13, a2: &v14, a3: v5);
          sub_1407C9510(a1: v15);
          sub_14083D820(a1: v17, a2: 256);
          sub_140835380(a1: v15, a2: 1768169504, a3: v17);
          sub_14083D320(a1: v17);
          (*(void (__fastcall **)(volatile signed __int32 *, _BYTE *))(*(_QWORD *)v14 + 16LL))(a1: v14, a2: v18);
          v7 = sub_1400015F0(a1: v18);
          sub_14083D970(a1: v17, a2: v7);
          sub_140835380(a1: v15, a2: 1952807028, a3: v17);
          sub_14083D320(a1: v17);
          sub_140808B00(a1: v18);
          sub_1407C9510(a1: v17);
          (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v14 + 16LL))(a1: v14, a2: v16);
          v8 = sub_1400015F0(a1: v16);
          sub_14083D970(a1: v18, a2: v8);
          sub_140835380(a1: v17, a2: 1835947128, a3: v18);
          sub_14083D320(a1: v18);
          sub_140808B00(a1: v16);
          sub_14083DDA0(a1: v18, a2: v15);
          sub_140835380(a1: v17, a2: 1986096245, a3: v18);
          sub_14083D320(a1: v18);
          sub_14083DDA0(a1: v18, a2: v17);
          sub_14083B5F0(a1, a2: v18);
          sub_14083D320(a1: v18);
          sub_140833970(a1: v17);
          result = sub_140833970(a1: v15);
          v9 = v14;
          if ( v14 != nullptr && _InterlockedDecrement(v14 + 2) == 0 )
            result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
        }
        while ( v5-- != 0 );
      }
      v10 = v13;
      if ( v13 != nullptr && _InterlockedDecrement(v13) == 0 )
      {
        sub_1400532D0(a1: v10);
        result = sub_141750CFC(a1: v10);
      }
    }
    v11 = v12;
    if ( v12 != nullptr && _InterlockedDecrement(v12 + 2) == 0 )
      return (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v11)(a1: v11, a2: 1);
    return result;
  }
  if ( v12 != nullptr && _InterlockedDecrement(v12 + 2) == 0 )
    result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v3)(a1: v3, a2: 1);
  v4 = v12;
  if ( v12 != nullptr )
    goto LABEL_12;
  return result;
}
