__int64 __fastcall sub_140FE8040(__int64 *a1, __int64 *a2)
{
  __int64 v3; // rdi
  __int64 v4; // rax
  __int64 result; // rax
  _BYTE v6[32]; // [rsp+28h] [rbp-20h] BYREF

  v3 = qword_141B5FE10;
  if ( (*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0 )
  {
    sub_140FE7960((__int64)v6, a2, 0x50657273u);
    v4 = sub_14002F670(v3, v6);
    if ( v4 != 0 )
      result = *(int *)(v4 + 8);
    else
      result = -1;
    goto LABEL_10;
  }
  sub_140FE7960((__int64)v6, a2, 0x50657273u);
  result = sub_14002F670(v3, v6);
  *a1 = result;
  if ( result != 0 && (_BYTE)word_141B60320 != 0 )
  {
    result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)result + 1816LL))(result);
    if ( result != 0 && (*(_BYTE *)(result + 103) & 7) == 0 )
    {
      result = 0;
LABEL_10:
      *a1 = result;
    }
  }
  return result;
}
