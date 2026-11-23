__int64 __fastcall sub_143955990(__int64 a1, __int16 a2, char a3)
{
  __int64 v6; // rbx
  __int64 result; // rax
  __int64 v8; // [rsp+28h] [rbp-30h] BYREF
  __int16 v9; // [rsp+30h] [rbp-28h]

  if ( byte_141B595A8 != 0 )
  {
    v6 = qword_141B595B0;
    result = (unsigned int)MEMORY[0x141947498](a1);
    if ( v6 != (unsigned int)result )
      return result;
  }
  else
  {
    result = (unsigned int)MEMORY[0x141947498](a1);
    if ( qword_141B5A658 != (unsigned int)result )
      return result;
  }
  *(_WORD *)(a1 + 2024) = a2;
  v8 = *(_QWORD *)(*(_QWORD *)(a1 + 2032) + 176LL);
  v9 = a2;
  result = sub_140A48250(
             *(_QWORD *)(a1 + 1976),
             *(_QWORD *)(a1 + 1984),
             (__int64)(*(_QWORD *)(a1 + 1984) - *(_QWORD *)(a1 + 1976)) >> 3,
             &v8);
  if ( a3 != 0 )
    return sub_1417513B0(*(_QWORD *)(a1 + 1976), *(_QWORD *)(a1 + 1984));
  return result;
}
