// THUNK ALIAS -> sub_14432BEC0 (jmp:0x14141fb00->0x14432bec0)
__int64 __fastcall sub_14432BEC0(unsigned int a1)
{
  __int64 v2; // rdi
  __int64 v3; // rdx
  BOOL v4; // ebp
  __int64 *v5; // rbx
  __int64 result; // rax
  unsigned int v7; // ecx
  __int64 *v8; // rdx
  __int64 v9; // rax
  __int64 *v10; // [rsp+28h] [rbp-30h] BYREF
  BOOL v11; // [rsp+30h] [rbp-28h]

  v2 = qword_141B63D28;
  v3 = *(_QWORD *)(qword_141B63D28 + 8);
  v4 = false;
  if ( *(_BYTE *)(v3 + 25) != 0 )
  {
    v5 = *(__int64 **)(qword_141B63D28 + 8);
    result = qword_141B63D28;
    if ( *(_BYTE *)(qword_141B63D28 + 25) == 0 )
      goto LABEL_9;
  }
  else
  {
    result = qword_141B63D28;
    do
    {
      v5 = (__int64 *)v3;
      v7 = *(_DWORD *)(v3 + 28);
      v8 = (__int64 *)(v3 + 16);
      if ( v7 >= a1 )
      {
        result = (__int64)v5;
        v8 = v5;
      }
      v3 = *v8;
    }
    while ( *(_BYTE *)(v3 + 25) == 0 );
    v4 = v7 >= a1;
    if ( *(_BYTE *)(result + 25) == 0 )
    {
LABEL_9:
      if ( *(_DWORD *)(result + 28) <= a1 )
        return result;
    }
  }
  if ( qword_141B63D30 == 0x7FFFFFFFFFFFFFFLL )
    sub_140052D20();
  v9 = sub_141750CC0(32);
  *(_DWORD *)(v9 + 28) = a1;
  *(_QWORD *)v9 = v2;
  *(_QWORD *)(v9 + 8) = v2;
  *(_QWORD *)(v9 + 16) = v2;
  *(_WORD *)(v9 + 24) = 0;
  v10 = v5;
  v11 = v4;
  return sub_140052AA0(&qword_141B63D28, &v10, v9);
}
