__int64 __fastcall sub_143C07D00(__int64 a1, volatile signed __int32 **a2)
{
  __int64 v2; // rdi
  volatile signed __int32 *v3; // rsi
  __int64 v4; // rdx
  char v5; // bl
  __int64 v6; // r14
  char v7; // bp
  __int64 v8; // r8
  _QWORD v10[6]; // [rsp+28h] [rbp-30h] BYREF

  v2 = a1;
  v3 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v3 + 2);
    v4 = a1 + 8;
    v5 = HIBYTE(qword_141B6034C);
    if ( (unsigned __int16)qword_141B60330 > 0xDC8u || HIBYTE(qword_141B6034C) != 0 )
    {
      v6 = a1 + 16;
      v7 = byte_141B5FC2C;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v3 + 40LL))(
        a1: v3,
        a2: v4,
        a3: 4);
      if ( v5 == 0 || (v8 = 13, v7 != 0) )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v3 + 40LL))(
          a1: v3,
          a2: v2 + 16,
          a3: 4);
        v8 = 5;
        v6 = v2 + 24;
      }
LABEL_14:
      v2 += 30;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v3 + 40LL))(
        a1: v3,
        a2: v6,
        a3: v8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v3 + 40LL))(
        a1: v3,
        a2: v2,
        a3: 2);
      goto LABEL_15;
    }
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v3 + 40LL))(a1: v3, a2: v4, a3: 4);
LABEL_7:
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v3 + 40LL))(
      a1: v3,
      a2: v10,
      a3: 8);
    if ( *((_DWORD *)v3 + 4) != 0 )
    {
      LODWORD(v2) = 0;
      if ( _InterlockedDecrement(v3 + 2) != 0 )
        return (unsigned int)v2;
      goto LABEL_16;
    }
    *(_QWORD *)(v2 + 16) = v10[0];
    v6 = v2 + 24;
    v8 = 5;
    goto LABEL_14;
  }
  if ( (unsigned __int16)qword_141B60330 <= 0xDC8u && HIBYTE(qword_141B6034C) == 0 )
    goto LABEL_7;
LABEL_15:
  LOBYTE(v2) = *((_DWORD *)v3 + 4) == 0;
  if ( _InterlockedDecrement(v3 + 2) == 0 )
LABEL_16:
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v3)(a1: v3, a2: 1);
  return (unsigned int)v2;
}
